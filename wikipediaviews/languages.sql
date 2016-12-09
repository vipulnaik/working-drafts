update `languages` set `datastart` = '20150701' where (not (`code` in (
  "en", # English
  "de", # German
  "fr", # French
  "pl", # Polish
  "ja", # Japanese
  "it", # Italian
  "nl", # Dutch
  "pt", # Portuguese
  "es", # Spanish
  "sv", # Swedish
  "ru", # Russian
  "zh", # Chinese
  "zh-classical", # Chinese (classical)
  "no", # Norwegian
  "fi", # Finnish
  "vo", # Volapük
  "ca", # Catalan
  "ro", # Romanian
  "tr", # Turkish
  "uk", # Ukrainian
  "eo", # Esperanto
  "cs", # Czech
  "hu", # Hungarian
  "sk", # Slovak
  "da", # Danish
  "id", # Indonesian
  "he", # Hebrew
  "lt", # Lithuanian
  "sr", # Serbian
  "sl", # Slovenian
  "ar", # Arabic
  "ko", # Korean
  "bg", # Bulgarian
  "et", # Estonian
  "new", # Newar / Nepal Bhasa
  "hr", # Croatian
  "te", # Telugu
  "ceb", # Cebuano
  "gl", # Galician
  "th", # Thai
  "el", # Greek
  "fa", # Persian
  "vi", # Vietnamese
  "nn", # Norwegian (Nynorsk)
  "ms", # Malay
  "simple", # Simple English
  "eu", # Basque
  "bpy", # Bishnupriya Manipuri
  "bs", # Bosnian
  "lb", # Luxembourgish
  "ka", # Georgian
  "is", # Icelandic
  "sq", # Albanian
  "br", # Breton
  "la", # Latin
  "az", # Azeri
  "bn", # Bengali
  "hi", # Hindi
  "mr", # Marathi
  "tl", # Tagalog
  "mk", # Macedonian
  "sh", # Serbo-Croatian
  "io", # Ido
  "cy", # Welsh
  "pms", # Piedmontese
  "su", # Sundanese
  "lv", # Latvian
  "ta", # Tamil
  "nap", # Neapolitan
  "jv", # Javanese
  "ht", # Haitian
  # MISSING: "Low nds", # Saxon
  "scn", # Sicilian
  "oc", # Occitan
  "ast", # Asturian
  "ku", # Kurdish
  "hy" # Armenian
)));

select * from languages where name in (
  'English',
  'German',
  'French',
  'Polish',
  'Japanese',
  'Italian',
  'Dutch',
  'Portuguese',
  'Spanish',
  'Swedish',
  'Russian',
  'Chinese',
  'Classical Chinese',
  'Norwegian',
  'Finnish',
  'Volapük',
  'Catalan',
  'Romanian',
  'Turkish',
  'Ukrainian',
  'Esperanto',
  'Czech',
  <option value="hu">Hungarian</option>
  <option value="sk">Slovak</option>
  <option value="da">Danish</option>
  <option value="id">Indonesian</option>
  <option value="he">Hebrew</option>
  <option value="lt">Lithuanian</option>
  <option value="sr">Serbian</option>
  <option value="sl">Slovenian</option>
  <option value="ar">Arabic</option>
  <option value="ko">Korean</option>
  <option value="bg">Bulgarian</option>
  <option value="et">Estonian</option>
  <option value="new">Newar / Nepal Bhasa</option>
  <option value="hr">Croatian</option>
  <option value="te">Telugu</option>
  <option value="ceb">Cebuano</option>
  <option value="gl">Galician</option>
  <option value="th">Thai</option>
  <option value="el">Greek</option>
  <option value="fa">Persian</option>
  <option value="vi">Vietnamese</option>
  <option value="nn">Norwegian (Nynorsk)</option>
  <option value="ms">Malay</option>
  <option value="simple">Simple English</option>
  <option value="eu">Basque</option>
  <option value="bpy">Bishnupriya Manipuri</option>
  <option value="bs">Bosnian</option>
  <option value="lb">Luxembourgish</option>
  <option value="ka">Georgian</option>
  <option value="is">Icelandic</option>
  <option value="sq">Albanian</option>
  <option value="br">Breton</option>
  <option value="la">Latin</option>
  <option value="az">Azeri</option>
  <option value="bn">Bengali</option>
  <option value="hi">Hindi</option>
  <option value="mr">Marathi</option>
  <option value="tl">Tagalog</option>
  <option value="mk">Macedonian</option>
  <option value="sh">Serbo-Croatian</option>
  <option value="io">Ido</option>
  <option value="cy">Welsh</option>
  <option value="pms">Piedmontese</option>
  <option value="su">Sundanese</option>
  <option value="lv">Latvian</option>
  <option value="ta">Tamil</option>
  <option value="nap">Neapolitan</option>
  <option value="jv">Javanese</option>
  <option value="ht">Haitian</option>
  <option value="Low nds">Saxon</option>
  <option value="scn">Sicilian</option>
  <option value="oc">Occitan</option>
  <option value="ast">Asturian</option>
  <option value="ku">Kurdish</option>
  <option value="hy">Armenian</option>
