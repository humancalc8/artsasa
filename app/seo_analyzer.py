import re
from collections import Counter
from html import unescape


# ============================================================
# ARTSASA BLOG SEO ANALYZER
# ============================================================
#
# Deterministic SEO analysis engine.
#
# Returns:
#
# {
#     "score": 0-100,
#     "rating": "...",
#     "checks": [...],
#     "recommendations": [...],
#     "metrics": {...}
# }
#
# The score is calculated from the actual blog content.
# No AI is required for the core score.
#
# ============================================================


# ============================================================
# SCORE WEIGHTS
# ============================================================

WEIGHTS = {
    "focus_keyword": 10,
    "seo_title": 10,
    "meta_description": 10,
    "content_length": 10,
    "slug": 7,
    "headings": 8,
    "keyword_usage": 8,
    "introduction": 5,
    "paragraphs": 5,
    "featured_image": 5,
    "image_alt": 5,
    "internal_links": 5,
    "external_links": 3,
    "readability": 5,
    "content_structure": 4,
}


# ============================================================
# TEXT UTILITIES
# ============================================================

def clean_text(value):
    """
    Convert a value into clean plain text.
    """

    if value is None:
        return ""

    value = unescape(str(value))

    # Remove HTML tags.
    value = re.sub(
        r"<[^>]+>",
        " ",
        value
    )

    # Normalize whitespace.
    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def html_text(value):
    """
    Preserve HTML for structural analysis.
    """

    if value is None:
        return ""

    return str(value)


def word_list(value):
    """
    Return normalized words.
    """

    text = clean_text(value).lower()

    return re.findall(
        r"\b[a-zA-ZÀ-ÿ0-9'-]+\b",
        text
    )


def word_count(value):
    return len(
        word_list(value)
    )


def normalize_keyword(keyword):
    """
    Normalize a focus keyword for matching.
    """

    return re.sub(
        r"\s+",
        " ",
        clean_text(keyword).lower()
    ).strip()


def contains_phrase(text, phrase):
    """
    Case-insensitive phrase search.
    """

    text = clean_text(text).lower()
    phrase = normalize_keyword(phrase)

    if not phrase:
        return False

    return phrase in text


def count_phrase(text, phrase):
    """
    Count occurrences of a phrase.
    """

    text = clean_text(text).lower()
    phrase = normalize_keyword(phrase)

    if not phrase:
        return 0

    return text.count(phrase)


# ============================================================
# HTML STRUCTURE
# ============================================================

def extract_headings(content):
    """
    Extract H1/H2/H3/H4/H5/H6 headings.
    """

    html = html_text(content)

    matches = re.findall(
        r"<h([1-6])[^>]*>(.*?)</h\1>",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    headings = []

    for level, text in matches:

        headings.append(
            {
                "level": int(level),
                "text": clean_text(text),
            }
        )

    return headings


def extract_links(content):
    """
    Extract href URLs from HTML.
    """

    html = html_text(content)

    return re.findall(
        r'<a[^>]+href=["\']([^"\']+)["\']',
        html,
        flags=re.IGNORECASE
    )


def extract_images(content):
    """
    Extract image information from HTML.
    """

    html = html_text(content)

    images = re.findall(
        r"<img\b([^>]*)>",
        html,
        flags=re.IGNORECASE
    )

    results = []

    for attributes in images:

        src_match = re.search(
            r'src=["\']([^"\']+)["\']',
            attributes,
            flags=re.IGNORECASE
        )

        alt_match = re.search(
            r'alt=["\']([^"\']*)["\']',
            attributes,
            flags=re.IGNORECASE
        )

        results.append(
            {
                "src": (
                    src_match.group(1)
                    if src_match
                    else ""
                ),
                "alt": (
                    alt_match.group(1).strip()
                    if alt_match
                    else ""
                ),
            }
        )

    return results


# ============================================================
# SENTENCE ANALYSIS
# ============================================================

def extract_sentences(text):
    """
    Basic sentence extraction.
    """

    text = clean_text(text)

    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def average_sentence_length(text):
    """
    Average number of words per sentence.
    """

    sentences = extract_sentences(text)

    if not sentences:
        return 0

    total_words = sum(
        word_count(sentence)
        for sentence in sentences
    )

    return round(
        total_words / len(sentences),
        1
    )


def long_sentence_ratio(text):
    """
    Percentage of sentences containing
    more than 25 words.
    """

    sentences = extract_sentences(text)

    if not sentences:
        return 0

    long_sentences = sum(
        1
        for sentence in sentences
        if word_count(sentence) > 25
    )

    return round(
        long_sentences / len(sentences) * 100,
        1
    )


# ============================================================
# CHECK RESULT
# ============================================================

def make_check(
    key,
    label,
    passed,
    points,
    message,
    recommendation=None,
):
    return {
        "key": key,
        "label": label,
        "passed": bool(passed),
        "points": points if passed else 0,
        "max_points": points,
        "message": message,
        "recommendation": recommendation,
    }


# ============================================================
# RATING
# ============================================================

def get_rating(score):

    if score >= 90:
        return "Excellent"

    if score >= 80:
        return "Very good"

    if score >= 70:
        return "Good"

    if score >= 50:
        return "Needs improvement"

    return "Poor"


# ============================================================
# FOCUS KEYWORD
# ============================================================

def check_focus_keyword(
    title,
    content,
    focus_keyword,
):

    keyword = normalize_keyword(
        focus_keyword
    )

    if not keyword:

        return make_check(
            "focus_keyword",
            "Focus keyword",
            False,
            WEIGHTS["focus_keyword"],
            "No focus keyword has been provided.",
            "Choose one clear search phrase for this article.",
        )

    title_has = contains_phrase(
        title,
        keyword
    )

    content_has = contains_phrase(
        content,
        keyword
    )

    passed = (
        title_has
        and content_has
    )

    if passed:

        message = (
            "The focus keyword appears in "
            "the title and article content."
        )

        recommendation = None

    elif title_has:

        message = (
            "The focus keyword is in the title "
            "but is missing from the article content."
        )

        recommendation = (
            "Use the focus keyword naturally "
            "in the article."
        )

    elif content_has:

        message = (
            "The focus keyword appears in the "
            "content but not in the title."
        )

        recommendation = (
            "Consider including the focus keyword "
            "naturally in the title."
        )

    else:

        message = (
            "The focus keyword was not found "
            "in the title or article."
        )

        recommendation = (
            "Use the focus keyword naturally in "
            "the title and body."
        )

    return make_check(
        "focus_keyword",
        "Focus keyword",
        passed,
        WEIGHTS["focus_keyword"],
        message,
        recommendation,
    )


# ============================================================
# SEO TITLE
# ============================================================

def check_seo_title(
    seo_title,
    focus_keyword,
):

    title = clean_text(
        seo_title
    )

    length = len(title)

    keyword_present = contains_phrase(
        title,
        focus_keyword
    )

    length_good = (
        45 <= length <= 65
    )

    passed = (
        bool(title)
        and length_good
        and keyword_present
    )

    if not title:

        message = (
            "No SEO title has been provided."
        )

        recommendation = (
            "Write a concise SEO title around "
            "50–60 characters."
        )

    elif not length_good:

        message = (
            f"SEO title is {length} characters."
        )

        recommendation = (
            "Aim for approximately 50–60 characters."
        )

    elif not keyword_present:

        message = (
            "The focus keyword is missing "
            "from the SEO title."
        )

        recommendation = (
            "Include the focus keyword naturally "
            "in the SEO title."
        )

    else:

        message = (
            f"SEO title is {length} characters "
            "and contains the focus keyword."
        )

        recommendation = None

    return make_check(
        "seo_title",
        "SEO title",
        passed,
        WEIGHTS["seo_title"],
        message,
        recommendation,
    )


# ============================================================
# META DESCRIPTION
# ============================================================

def check_meta_description(
    meta_description,
    focus_keyword,
):

    description = clean_text(
        meta_description
    )

    length = len(description)

    keyword_present = contains_phrase(
        description,
        focus_keyword
    )

    length_good = (
        140 <= length <= 165
    )

    passed = (
        bool(description)
        and length_good
        and keyword_present
    )

    if not description:

        message = (
            "No meta description has been provided."
        )

        recommendation = (
            "Write a useful meta description "
            "around 150–160 characters."
        )

    elif not length_good:

        message = (
            f"Meta description is {length} characters."
        )

        recommendation = (
            "Aim for approximately 150–160 characters."
        )

    elif not keyword_present:

        message = (
            "The focus keyword is missing "
            "from the meta description."
        )

        recommendation = (
            "Include the focus keyword naturally."
        )

    else:

        message = (
            f"Meta description is {length} characters "
            "and contains the focus keyword."
        )

        recommendation = None

    return make_check(
        "meta_description",
        "Meta description",
        passed,
        WEIGHTS["meta_description"],
        message,
        recommendation,
    )


# ============================================================
# CONTENT LENGTH
# ============================================================

def check_content_length(content):

    count = word_count(
        content
    )

    passed = (
        count >= 600
    )

    if count >= 1000:

        message = (
            f"{count:,} words. The article has "
            "substantial depth."
        )

    elif count >= 600:

        message = (
            f"{count:,} words. The article "
            "has a useful minimum length."
        )

    else:

        message = (
            f"{count:,} words. The article "
            "may need more useful depth."
        )

    recommendation = (
        None
        if passed
        else
        "Expand the article with genuinely "
        "useful information rather than filler."
    )

    return make_check(
        "content_length",
        "Content length",
        passed,
        WEIGHTS["content_length"],
        message,
        recommendation,
    )


# ============================================================
# SLUG
# ============================================================

def check_slug(
    slug,
    focus_keyword,
):

    slug = clean_text(
        slug
    ).lower()

    keyword = normalize_keyword(
        focus_keyword
    )

    slug_has_keyword = (
        keyword.replace(" ", "-")
        in slug
        if keyword
        else False
    )

    clean_slug = bool(
        re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*",
            slug
        )
    )

    reasonable_length = (
        len(slug) <= 75
    )

    passed = (
        bool(slug)
        and clean_slug
        and reasonable_length
        and slug_has_keyword
    )

    if not slug:

        message = "No URL slug has been provided."

        recommendation = (
            "Create a short, descriptive SEO-friendly slug."
        )

    elif not clean_slug:

        message = (
            "The slug contains characters or "
            "formatting that should be cleaned."
        )

        recommendation = (
            "Use lowercase words separated by hyphens."
        )

    elif not reasonable_length:

        message = (
            f"The slug is {len(slug)} characters long."
        )

        recommendation = (
            "Shorten the slug to keep the URL focused."
        )

    elif not slug_has_keyword:

        message = (
            "The focus keyword is not reflected "
            "in the slug."
        )

        recommendation = (
            "Where natural, include the main topic "
            "in the slug."
        )

    else:

        message = (
            "The slug is clean, concise and "
            "aligned with the focus keyword."
        )

        recommendation = None

    return make_check(
        "slug",
        "SEO-friendly slug",
        passed,
        WEIGHTS["slug"],
        message,
        recommendation,
    )


# ============================================================
# HEADINGS
# ============================================================

def check_headings(content):

    headings = extract_headings(
        content
    )

    h2_count = sum(
        1
        for heading in headings
        if heading["level"] == 2
    )

    h3_count = sum(
        1
        for heading in headings
        if heading["level"] == 3
    )

    passed = (
        2 <= h2_count <= 8
    )

    if not headings:

        message = (
            "The article does not contain "
            "structured headings."
        )

        recommendation = (
            "Break the article into meaningful H2 sections."
        )

    elif h2_count < 2:

        message = (
            f"Only {h2_count} H2 heading found."
        )

        recommendation = (
            "Use several descriptive H2 sections "
            "to organize the article."
        )

    elif h2_count > 8:

        message = (
            f"{h2_count} H2 headings found. "
            "The article may be over-segmented."
        )

        recommendation = (
            "Combine closely related sections where appropriate."
        )

    else:

        message = (
            f"{h2_count} H2 headings and "
            f"{h3_count} H3 headings found."
        )

        recommendation = None

    return make_check(
        "headings",
        "Heading structure",
        passed,
        WEIGHTS["headings"],
        message,
        recommendation,
    )


# ============================================================
# KEYWORD USAGE
# ============================================================

def check_keyword_usage(
    content,
    focus_keyword,
):

    keyword = normalize_keyword(
        focus_keyword
    )

    if not keyword:

        return make_check(
            "keyword_usage",
            "Keyword usage",
            False,
            WEIGHTS["keyword_usage"],
            "No focus keyword available for density analysis.",
            "Choose a focus keyword.",
        )

    count = count_phrase(
        content,
        keyword
    )

    total_words = word_count(
        content
    )

    if not total_words:

        density = 0

    else:

        keyword_words = max(
            1,
            len(
                keyword.split()
            )
        )

        density = (
            count
            * keyword_words
            / total_words
            * 100
        )

    density = round(
        density,
        2
    )

    passed = (
        0.3 <= density <= 2.5
        and count >= 2
    )

    if count == 0:

        message = (
            "The focus keyword does not appear "
            "in the article."
        )

        recommendation = (
            "Use the keyword naturally where it "
            "helps answer the reader's question."
        )

    elif density > 2.5:

        message = (
            f"Keyword density is {density}%. "
            "This may be excessive."
        )

        recommendation = (
            "Reduce repetition and use natural "
            "language and related terms."
        )

    elif density < 0.3:

        message = (
            f"Keyword density is {density}%. "
            "The topic may not be clearly signalled."
        )

        recommendation = (
            "Use the focus keyword a few natural "
            "times where relevant."
        )

    else:

        message = (
            f"Keyword appears {count} times "
            f"({density}% estimated density)."
        )

        recommendation = None

    return make_check(
        "keyword_usage",
        "Keyword usage",
        passed,
        WEIGHTS["keyword_usage"],
        message,
        recommendation,
    )


# ============================================================
# INTRODUCTION
# ============================================================

def check_introduction(
    content,
    focus_keyword,
):

    text = clean_text(
        content
    )

    words = text.split()

    first_words = " ".join(
        words[:120]
    )

    passed = (
        contains_phrase(
            first_words,
            focus_keyword
        )
    )

    if passed:

        message = (
            "The focus keyword appears early "
            "in the article."
        )

        recommendation = None

    else:

        message = (
            "The focus keyword does not appear "
            "in the opening section."
        )

        recommendation = (
            "Introduce the article's main topic "
            "naturally near the beginning."
        )

    return make_check(
        "introduction",
        "Keyword in introduction",
        passed,
        WEIGHTS["introduction"],
        message,
        recommendation,
    )


# ============================================================
# PARAGRAPHS
# ============================================================

def check_paragraphs(content):

    html = html_text(
        content
    )

    paragraphs = re.findall(
        r"<p[^>]*>(.*?)</p>",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    if not paragraphs:

        return make_check(
            "paragraphs",
            "Paragraph structure",
            False,
            WEIGHTS["paragraphs"],
            "No HTML paragraphs were detected.",
            "Use clear paragraphs to make the article easier to read.",
        )

    paragraph_lengths = [
        word_count(paragraph)
        for paragraph in paragraphs
    ]

    long_paragraphs = sum(
        1
        for length in paragraph_lengths
        if length > 120
    )

    passed = (
        long_paragraphs
        <= max(
            1,
            len(paragraphs) // 5
        )
    )

    if passed:

        message = (
            f"{len(paragraphs)} paragraphs detected "
            "with reasonable paragraph lengths."
        )

        recommendation = None

    else:

        message = (
            f"{long_paragraphs} paragraphs are "
            "particularly long."
        )

        recommendation = (
            "Break long paragraphs into smaller "
            "reader-friendly sections."
        )

    return make_check(
        "paragraphs",
        "Paragraph structure",
        passed,
        WEIGHTS["paragraphs"],
        message,
        recommendation,
    )


# ============================================================
# FEATURED IMAGE
# ============================================================

def check_featured_image(
    featured_image=None,
):

    passed = bool(
        featured_image
    )

    if passed:

        message = (
            "A featured image is assigned."
        )

        recommendation = None

    else:

        message = (
            "No featured image is assigned."
        )

        recommendation = (
            "Add a relevant, high-quality featured image."
        )

    return make_check(
        "featured_image",
        "Featured image",
        passed,
        WEIGHTS["featured_image"],
        message,
        recommendation,
    )


# ============================================================
# IMAGE ALT
# ============================================================

def check_image_alt(
    featured_image=None,
    image_alt="",
    content="",
):

    alt = clean_text(
        image_alt
    )

    images = extract_images(
        content
    )

    if featured_image and alt:

        passed = True

        message = (
            "The featured image has descriptive ALT text."
        )

        recommendation = None

    elif featured_image:

        passed = False

        message = (
            "The featured image does not have "
            "descriptive ALT text."
        )

        recommendation = (
            "Write concise ALT text describing "
            "the image and its relevance."
        )

    elif images:

        images_without_alt = sum(
            1
            for image in images
            if not image["alt"]
        )

        passed = (
            images_without_alt == 0
        )

        message = (
            f"{len(images)} content images detected; "
            f"{images_without_alt} have missing ALT text."
        )

        recommendation = (
            None
            if passed
            else
            "Add meaningful ALT text to informative images."
        )

    else:

        passed = False

        message = (
            "No image information was detected."
        )

        recommendation = (
            "Add a relevant featured image with "
            "descriptive ALT text."
        )

    return make_check(
        "image_alt",
        "Image ALT text",
        passed,
        WEIGHTS["image_alt"],
        message,
        recommendation,
    )


# ============================================================
# INTERNAL LINKS
# ============================================================

def check_internal_links(content):

    links = extract_links(
        content
    )

    internal_links = [
        link
        for link in links
        if (
            link.startswith("/")
            or "artsasa" in link.lower()
        )
    ]

    passed = (
        len(internal_links) >= 1
    )

    if passed:

        message = (
            f"{len(internal_links)} internal "
            "link(s) detected."
        )

        recommendation = None

    else:

        message = (
            "No internal links were detected."
        )

        recommendation = (
            "Link naturally to relevant ARTSASA "
            "artists, artworks, exhibitions or articles."
        )

    return make_check(
        "internal_links",
        "Internal links",
        passed,
        WEIGHTS["internal_links"],
        message,
        recommendation,
    )


# ============================================================
# EXTERNAL LINKS
# ============================================================

def check_external_links(content):

    links = extract_links(
        content
    )

    external_links = [
        link
        for link in links
        if link.startswith(
            (
                "http://",
                "https://",
            )
        )
        and "artsasa" not in link.lower()
    ]

    passed = (
        len(external_links) >= 1
    )

    if passed:

        message = (
            f"{len(external_links)} external "
            "reference link(s) detected."
        )

        recommendation = None

    else:

        message = (
            "No external reference links were detected."
        )

        recommendation = (
            "Where appropriate, cite useful authoritative "
            "sources rather than adding links purely for SEO."
        )

    return make_check(
        "external_links",
        "External references",
        passed,
        WEIGHTS["external_links"],
        message,
        recommendation,
    )


# ============================================================
# READABILITY
# ============================================================

def check_readability(content):

    text = clean_text(
        content
    )

    avg_sentence = average_sentence_length(
        text
    )

    long_ratio = long_sentence_ratio(
        text
    )

    passed = (
        avg_sentence <= 25
        and long_ratio <= 25
    )

    if passed:

        message = (
            f"Average sentence length is "
            f"{avg_sentence} words; "
            f"{long_ratio}% are over 25 words."
        )

        recommendation = None

    else:

        message = (
            f"Average sentence length is "
            f"{avg_sentence} words; "
            f"{long_ratio}% are over 25 words."
        )

        recommendation = (
            "Shorten long sentences and use clearer "
            "sentence structure."
        )

    return make_check(
        "readability",
        "Readability",
        passed,
        WEIGHTS["readability"],
        message,
        recommendation,
    )


# ============================================================
# CONTENT STRUCTURE
# ============================================================

def check_content_structure(content):

    headings = extract_headings(
        content
    )

    has_lists = bool(
        re.search(
            r"<(?:ul|ol)\b",
            html_text(content),
            flags=re.IGNORECASE
        )
    )

    has_headings = len(
        headings
    ) >= 2

    passed = (
        has_headings
        and has_lists
    )

    if passed:

        message = (
            "The article uses headings and "
            "list-based structure."
        )

        recommendation = None

    elif has_headings:

        message = (
            "The article has headings but "
            "could benefit from more varied structure."
        )

        recommendation = (
            "Use lists where they genuinely improve "
            "clarity."
        )

    else:

        message = (
            "The article has limited structural markup."
        )

        recommendation = (
            "Use meaningful headings and lists "
            "where appropriate."
        )

    return make_check(
        "content_structure",
        "Content structure",
        passed,
        WEIGHTS["content_structure"],
        message,
        recommendation,
    )


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_blog(
    *,
    title="",
    slug="",
    excerpt="",
    content="",
    focus_keyword="",
    seo_title="",
    meta_description="",
    featured_image=None,
    image_alt="",
):

    title = clean_text(
        title
    )

    slug = clean_text(
        slug
    )

    excerpt = clean_text(
        excerpt
    )

    content = html_text(
        content
    )

    focus_keyword = clean_text(
        focus_keyword
    )

    seo_title = clean_text(
        seo_title
    )

    meta_description = clean_text(
        meta_description
    )

    checks = []

    checks.append(
        check_focus_keyword(
            title,
            content,
            focus_keyword,
        )
    )

    checks.append(
        check_seo_title(
            seo_title,
            focus_keyword,
        )
    )

    checks.append(
        check_meta_description(
            meta_description,
            focus_keyword,
        )
    )

    checks.append(
        check_content_length(
            content
        )
    )

    checks.append(
        check_slug(
            slug,
            focus_keyword,
        )
    )

    checks.append(
        check_headings(
            content
        )
    )

    checks.append(
        check_keyword_usage(
            content,
            focus_keyword,
        )
    )

    checks.append(
        check_introduction(
            content,
            focus_keyword,
        )
    )

    checks.append(
        check_paragraphs(
            content
        )
    )

    checks.append(
        check_featured_image(
            featured_image
        )
    )

    checks.append(
        check_image_alt(
            featured_image,
            image_alt,
            content,
        )
    )

    checks.append(
        check_internal_links(
            content
        )
    )

    checks.append(
        check_external_links(
            content
        )
    )

    checks.append(
        check_readability(
            content
        )
    )

    checks.append(
        check_content_structure(
            content
        )
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    earned = sum(
        check["points"]
        for check in checks
    )

    maximum = sum(
        check["max_points"]
        for check in checks
    )

    if maximum:

        score = round(
            earned / maximum * 100
        )

    else:

        score = 0

    score = max(
        0,
        min(
            100,
            score
        )
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = []

    for check in checks:

        recommendation = check.get(
            "recommendation"
        )

        if recommendation:

            recommendations.append(
                {
                    "key": check["key"],
                    "label": check["label"],
                    "text": recommendation,
                }
            )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    headings = extract_headings(
        content
    )

    links = extract_links(
        content
    )

    images = extract_images(
        content
    )

    metrics = {
        "word_count": word_count(content),
        "title_length": len(title),
        "seo_title_length": len(seo_title),
        "meta_description_length": len(meta_description),
        "slug_length": len(slug),
        "focus_keyword": focus_keyword,
        "keyword_occurrences": count_phrase(
            content,
            focus_keyword
        ),
        "heading_count": len(headings),
        "h2_count": sum(
            1
            for heading in headings
            if heading["level"] == 2
        ),
        "h3_count": sum(
            1
            for heading in headings
            if heading["level"] == 3
        ),
        "link_count": len(links),
        "image_count": len(images),
        "average_sentence_length": average_sentence_length(
            clean_text(content)
        ),
        "long_sentence_percentage": long_sentence_ratio(
            clean_text(content)
        ),
    }

    return {
        "score": score,
        "rating": get_rating(score),
        "checks": checks,
        "recommendations": recommendations,
        "metrics": metrics,
    }