# Download the World English Bible (WEB) and split into per-book JSON files
# Source: https://github.com/TehShrike/world-english-bible (public domain / CC0)
# Output: roku/src/data/books/{abbrev}.json  (one file per book, 66 total)

$baseUrl = "https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json"
$outDir  = "$PSScriptRoot\..\roku\src\data\books"

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# Mapping: TehShrike filename -> [display name, abbreviation]
$books = [ordered]@{
    "genesis"         = @("Genesis",          "gn")
    "exodus"          = @("Exodus",           "ex")
    "leviticus"       = @("Leviticus",        "lv")
    "numbers"         = @("Numbers",          "nm")
    "deuteronomy"     = @("Deuteronomy",      "dt")
    "joshua"          = @("Joshua",           "js")
    "judges"          = @("Judges",           "jdg")
    "ruth"            = @("Ruth",             "rt")
    "1samuel"         = @("1 Samuel",         "1sm")
    "2samuel"         = @("2 Samuel",         "2sm")
    "1kings"          = @("1 Kings",          "1kgs")
    "2kings"          = @("2 Kings",          "2kgs")
    "1chronicles"     = @("1 Chronicles",     "1ch")
    "2chronicles"     = @("2 Chronicles",     "2ch")
    "ezra"            = @("Ezra",             "ezr")
    "nehemiah"        = @("Nehemiah",         "ne")
    "esther"          = @("Esther",           "est")
    "job"             = @("Job",              "jb")
    "psalms"          = @("Psalms",           "ps")
    "proverbs"        = @("Proverbs",         "prv")
    "ecclesiastes"    = @("Ecclesiastes",     "ec")
    "songofsolomon"   = @("Song of Solomon",  "sg")
    "isaiah"          = @("Isaiah",           "is")
    "jeremiah"        = @("Jeremiah",         "jr")
    "lamentations"    = @("Lamentations",     "lm")
    "ezekiel"         = @("Ezekiel",          "ez")
    "daniel"          = @("Daniel",           "dn")
    "hosea"           = @("Hosea",            "hs")
    "joel"            = @("Joel",             "jl")
    "amos"            = @("Amos",             "am")
    "obadiah"         = @("Obadiah",          "ob")
    "jonah"           = @("Jonah",            "jon")
    "micah"           = @("Micah",            "mc")
    "nahum"           = @("Nahum",            "na")
    "habakkuk"        = @("Habakkuk",         "hbk")
    "zephaniah"       = @("Zephaniah",        "zp")
    "haggai"          = @("Haggai",           "hg")
    "zechariah"       = @("Zechariah",        "zc")
    "malachi"         = @("Malachi",          "ml")
    "matthew"         = @("Matthew",          "mt")
    "mark"            = @("Mark",             "mk")
    "luke"            = @("Luke",             "lk")
    "john"            = @("John",             "jn")
    "acts"            = @("Acts",             "act")
    "romans"          = @("Romans",           "rm")
    "1corinthians"    = @("1 Corinthians",    "1co")
    "2corinthians"    = @("2 Corinthians",    "2co")
    "galatians"       = @("Galatians",        "gl")
    "ephesians"       = @("Ephesians",        "eph")
    "philippians"     = @("Philippians",      "ph")
    "colossians"      = @("Colossians",       "cl")
    "1thessalonians"  = @("1 Thessalonians",  "1ts")
    "2thessalonians"  = @("2 Thessalonians",  "2ts")
    "1timothy"        = @("1 Timothy",        "1tm")
    "2timothy"        = @("2 Timothy",        "2tm")
    "titus"           = @("Titus",            "tt")
    "philemon"        = @("Philemon",         "phm")
    "hebrews"         = @("Hebrews",          "hb")
    "james"           = @("James",            "jms")
    "1peter"          = @("1 Peter",          "1pt")
    "2peter"          = @("2 Peter",          "2pt")
    "1john"           = @("1 John",           "1jn")
    "2john"           = @("2 John",           "2jn")
    "3john"           = @("3 John",           "3jn")
    "jude"            = @("Jude",             "jd")
    "revelation"      = @("Revelation",       "rv")
}

$total = $books.Count
$count = 0

foreach ($filename in $books.Keys) {
    $count++
    $displayName = $books[$filename][0]
    $abbrev      = $books[$filename][1]

    $url = "$baseUrl/$filename.json"
    Write-Host "[$count/$total] Downloading $displayName..."

    try {
        $raw = Invoke-RestMethod -Uri $url -UseBasicParsing
    } catch {
        Write-Warning "  FAILED to download $filename.json: $_"
        continue
    }

    # Filter to only entries that have verse text
    $textEntries = $raw | Where-Object { $null -ne $_.value }

    # Group by chapter, then verse, joining sections of the same verse
    $chapterGroups = $textEntries | Group-Object chapterNumber | Sort-Object { [int]$_.Name }

    $chapters = @()
    foreach ($cg in $chapterGroups) {
        $verseGroups = $cg.Group | Group-Object verseNumber | Sort-Object { [int]$_.Name }
        $verses = @()
        foreach ($vg in $verseGroups) {
            $text = ($vg.Group | Sort-Object sectionNumber | ForEach-Object { $_.value.Trim() }) -join " "
            $text = $text -replace '\s+', ' '
            $verses += [ordered]@{
                verse = [int]$vg.Name
                text  = $text.Trim()
            }
        }
        $chapters += [ordered]@{
            chapter = [int]$cg.Name
            verses  = $verses
        }
    }

    $bookObj = [ordered]@{
        book     = $displayName
        abbrev   = $abbrev
        chapters = $chapters
    }

    $filePath = Join-Path $outDir "$abbrev.json"
    $bookObj | ConvertTo-Json -Depth 10 -Compress | Set-Content -Path $filePath -Encoding UTF8
    Write-Host "  -> $abbrev.json ($($chapters.Count) chapters)"
}

Write-Host ""
Write-Host "Done! $total books written to: $outDir"
