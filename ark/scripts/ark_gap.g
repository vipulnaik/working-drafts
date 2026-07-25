# ark_gap.g -- enumerate permutation groups on [1..N] for the ARK CSP
# (N set below; tested at 10, designed for 12).
#
# Output: one line per group in groups_out.txt, format
#     KEY|DESC|OLIVERQ|ORBMAP
#   KEY     unique checkpoint key (also written to done_keys.txt)
#   DESC    human-readable description
#   OLIVERQ top prime q of a valid Oliver chain, 0 if top layer can be trivial
#           (chi = 1 exactly), or P<p> for pure p-groups (Smith battery)
#   ORBMAP  45 comma-separated integers: for each pair {i<j} of [1..10] in
#           lexicographic order ((1,2),(1,3),...,(9,10)), the orbital index
#           (1-based) of that pair under the group.
#
# Anytime-stoppable: each completed item appends its KEY to done_keys.txt and
# its data line to groups_out.txt; on restart, completed KEYs are skipped.
# Safe to Ctrl-C between items (worst case: one item recomputed).
# Progress is logged to ark_gap.log with millisecond runtimes.
#
# Stages (edit STAGES below to select; each is independent):
#   "A"    transitive groups of degree 10 (library; 45 groups)      ~minutes
#   "B"    direct products of transitive groups over partitions      ~minutes
#   "B2"   imprimitive wreath products for 10 = 2*5 and 5*2          ~minutes
#   "C"    p-subgroups: all subgroups of Sylow_p(S10), p=2,3,5,7     ~min-hours
#   "FULL" ALL subgroup classes of S10, filtered to Oliver           HEAVY; off
#
# Tunables:
# DEGREE: taken from the ARK_N environment variable, default 10.
# Usage:   ARK_N=12 gap -q -o 4g /path/to/ark_gap.g     (run from the
# per-degree working directory; all output files are written to the CWD).
if IsBound(GAPInfo.SystemEnvironment.ARK_N) then
  N := Int(GAPInfo.SystemEnvironment.ARK_N);;
else
  N := 10;;
fi;;
Print("ark_gap.g running with degree N = ", N, "\n");
STAGES  := [ "A", "B", "B2", "C" ];;
MAXT    := 12;;   # skip groups with more than MAXT u-orbitals (CSP cost 2^t)
MAXPARTS:= 4;;    # stage B: max number of parts in the partition
OUTFILE := "groups_out.txt";;
DONEFILE:= "done_keys.txt";;
LOGFILE := "ark_gap.log";;

# ---------------------------------------------------------------- utilities
LoadPackage("transgrp");   # transitive groups library; usually bundled

PAIRS := Combinations([1..N], 2);;   # lexicographic, length C(N,2)

Log := function(msg)
  AppendTo(LOGFILE, String(Runtime()), "ms  ", msg, "\n");
  Print(msg, "\n");
end;;

ReadDone := function()
  local s, done, line;
  done := rec();
  if IsExistingFile(DONEFILE) then
    s := StringFile(DONEFILE);           # StringFile is from GAPDoc (standard)
    for line in SplitString(s, "\n") do
      if Length(line) > 0 then done.(line) := true; fi;
    od;
  fi;
  return done;
end;;

DONE := ReadDone();;
Log(Concatenation("resuming with ", String(Length(RecNames(DONE))), " done keys"));

OrbMap := function(G)
  local orbs, map, i, o, p;
  orbs := Orbits(G, PAIRS, OnSets);
  map := [];
  for i in [1..Length(orbs)] do
    for p in orbs[i] do
      map[PositionSorted(PAIRS, p)] := i;
    od;
  od;
  return rec(map := map, t := Length(orbs));
end;;

# Oliver's condition: exists N normal in G with G/N a q-group (or trivial),
# and N/O_p(N) cyclic for some prime p (or N trivial).  Returns:
#   fail  if not Oliver
#   0     if achievable with trivial top layer (chi = 1 exactly)
#   q     the smallest usable top prime otherwise
IsOliverTop := function(G)
  local best, N, Q, q, p, ok;
  if Size(G) = 1 then return 0; fi;
  best := fail;
  for N in NormalSubgroups(G) do
    # bottom+middle check on N
    ok := Size(N) = 1;
    if not ok then
      for p in PrimeDivisors(Size(N)) do
        if IsCyclic(FactorGroup(N, PCore(N, p))) then ok := true; break; fi;
      od;
    fi;
    if not ok then continue; fi;
    if Size(N) = Size(G) then
      return 0;                              # trivial top: strongest
    fi;
    Q := FactorGroup(G, N);
    if IsPGroup(Q) then
      q := PrimePGroup(Q);
      if best = fail or q < best then best := q; fi;
    fi;
  od;
  return best;
end;;

EmitGroup := function(key, desc, G)
  local om, tag, oq;
  if IsBound(DONE.(key)) then return; fi;
  om := OrbMap(G);
  if om.t > MAXT then
    AppendTo(DONEFILE, key, "\n"); DONE.(key) := true;
    return;                                  # skipped (too many orbitals)
  fi;
  if IsPGroup(G) and Size(G) > 1 then
    tag := Concatenation("P", String(PrimePGroup(G)));   # Smith battery entry
  else
    oq := IsOliverTop(G);
    if oq = fail then
      AppendTo(DONEFILE, key, "\n"); DONE.(key) := true;
      return;                                # not Oliver: skip
    fi;
    tag := String(oq);
  fi;
  AppendTo(OUTFILE, key, "|", desc, "|", tag, "|",
           JoinStringsWithSeparator(List(om.map, String), ","), "\n");
  AppendTo(DONEFILE, key, "\n");
  DONE.(key) := true;
  Log(Concatenation("emitted ", key, "  t=", String(om.t), "  tag=", tag));
end;;

# ---------------------------------------------------------------- stage A
if "A" in STAGES then
  Log("=== stage A: transitive groups of degree 10 ===");
  for k in [1..NrTransitiveGroups(N)] do
    EmitGroup(Concatenation("A:", String(k)),
              Concatenation("T(", String(N), ",", String(k), ") order ",
                            String(Size(TransitiveGroup(N,k)))),
              TransitiveGroup(N, k));
  od;
  Log("stage A complete");
fi;

# ---------------------------------------------------------------- stage B
# direct products of transitive groups over partitions of 10 (parts >= 1);
# part of size 1 contributes the trivial group.
if "B" in STAGES then
  Log("=== stage B: direct products over partitions ===");
  for part in Partitions(N) do
    if Length(part) < 2 or Length(part) > MAXPARTS then continue; fi;
    # index ranges per part (size-1 parts: single trivial choice)
    ranges := List(part, d -> Maximum(1, NrTransitiveGroups(Maximum(d,2))));
    ranges := List([1..Length(part)],
                   i -> Filtered([1..ranges[i]],
                        k -> part[i] > 1 or k = 1));
    for combo in Cartesian(ranges) do
      key := Concatenation("B:", JoinStringsWithSeparator(List(part,String),"+"),
                           ":", JoinStringsWithSeparator(List(combo,String),"."));
      if IsBound(DONE.(key)) then continue; fi;
      gens := []; off := 0;
      for i in [1..Length(part)] do
        d := part[i];
        if d > 1 then
          T := TransitiveGroup(d, combo[i]);
          for g in GeneratorsOfGroup(T) do
            Add(gens, PermList(Concatenation([1..off],
                    List([1..d], x -> off + x^g),
                    [off+d+1..N])));
          od;
        fi;
        off := off + d;
      od;
      if Length(gens) = 0 then continue; fi;
      EmitGroup(key,
        Concatenation("prod ", JoinStringsWithSeparator(List(part,String),"+")),
        Group(gens));
    od;
    Log(Concatenation("stage B partition ",
        JoinStringsWithSeparator(List(part,String),"+"), " done"));
  od;
  Log("stage B complete");
fi;

# ---------------------------------------------------------------- stage B2
# imprimitive wreath products G wr H on 10 = d*r points
if "B2" in STAGES then
  Log("=== stage B2: imprimitive wreath products ===");
  wr_pairs := [];;
  for d in [2..N-1] do
    if N mod d = 0 and N/d >= 2 then Add(wr_pairs, [d, N/d]); fi;
  od;
  for dr in wr_pairs do
    d := dr[1]; r := dr[2];
    for k in [1..NrTransitiveGroups(Maximum(d,2))] do
      for j in [1..NrTransitiveGroups(Maximum(r,2))] do
        key := Concatenation("B2:", String(d), "x", String(r), ":",
                             String(k), ".", String(j));
        if IsBound(DONE.(key)) then continue; fi;
        W := WreathProduct(TransitiveGroup(d,k), TransitiveGroup(r,j));
        EmitGroup(key,
          Concatenation("T(",String(d),",",String(k),") wr T(",
                        String(r),",",String(j),")"), W);
      od;
    od;
  od;
  Log("stage B2 complete");
fi;

# ---------------------------------------------------------------- stage C
# all subgroups (up to Sylow-conjugacy) of each Sylow_p(S10): Smith battery
if "C" in STAGES then
  Log("=== stage C: p-subgroups of Sylow subgroups ===");
  SN := SymmetricGroup(N);
  for p in Filtered(Primes, q -> q <= N) do
    key0 := Concatenation("C:", String(p), ":ALLDONE");
    if IsBound(DONE.(key0)) then
      Log(Concatenation("stage C p=", String(p), " already done"));
      continue;
    fi;
    P := SylowSubgroup(SN, p);
    Log(Concatenation("Sylow_", String(p), " order ", String(Size(P)),
                      "; computing subgroup classes (may take a while for p=2)"));
    ccs := ConjugacyClassesSubgroups(P);
    Log(Concatenation("  ", String(Length(ccs)), " classes"));
    for i in [1..Length(ccs)] do
      H := Representative(ccs[i]);
      if Size(H) > 1 then
        EmitGroup(Concatenation("C:", String(p), ":", String(i)),
                  Concatenation("p", String(p), "-subgroup #", String(i),
                                " order ", String(Size(H))), H);
      fi;
    od;
    AppendTo(DONEFILE, key0, "\n"); DONE.(key0) := true;
    Log(Concatenation("stage C p=", String(p), " complete"));
  od;
fi;

# ---------------------------------------------------------------- stage FULL
# every subgroup class of S10, filtered to Oliver.  VERY heavy (hours, GB of
# RAM).  Run only on a machine you can leave alone; the single call
# ConjugacyClassesSubgroups(S10) is not checkpointable -- if it completes,
# per-group emission below is checkpointed as usual.
if "FULL" in STAGES then
  Log("=== stage FULL: all subgroup classes of S10 (heavy) ===");
  SN := SymmetricGroup(N);
  ccs := ConjugacyClassesSubgroups(SN);
  Log(Concatenation(String(Length(ccs)), " subgroup classes"));
  for i in [1..Length(ccs)] do
    H := Representative(ccs[i]);
    if Size(H) > 1 then
      EmitGroup(Concatenation("F:", String(i)),
                Concatenation("SN subgroup #", String(i),
                              " order ", String(Size(H))), H);
    fi;
    if i mod 200 = 0 then Log(Concatenation("FULL progress ", String(i))); fi;
  od;
  Log("stage FULL complete");
fi;

Log("ALL SELECTED STAGES COMPLETE");
QUIT;
