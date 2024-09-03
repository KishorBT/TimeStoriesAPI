import http.client

def fetch_html(url):
    conn = http.client.HTTPSConnection("time.com")
    conn.request("GET", url)
    response = conn.getresponse()
    if response.status == 200:
        html = response.read().decode('utf-8')
        conn.close()
        return html
    else:
        conn.close()
        print(f"Error fetching page: {response.status} {response.reason}")
        return None

def get_latest_stories(html):
    stories = []
    start_marker = '<h2 class="latest-stories__item-headline">'
    link_marker = '<a href="'
    end_marker = '</h2>'

    start_pos = 0

    while len(stories) < 6:
        start_pos = html.find(start_marker, start_pos)
        if start_pos == -1:
            break

        link_start = html.find(link_marker, start_pos) + len(link_marker)
        link_end = html.find('"', link_start)
        link = "https://time.com" + html[link_start:link_end]

        title_start = link_end + 2
        title_end = html.find(end_marker, title_start)
        title = html[title_start:title_end].strip()

        stories.append({"title": title, "link": link})

        start_pos = title_end

    return stories

def main():
    url = '/'
    html_content = fetch_html(url)
    if html_content:
        # Debug: print raw HTML content
        print("HTML Content Received:")
        print(html_content[:2000])  # Print first 2000 characters for inspection
        
        latest_stories = get_latest_stories(html_content)
        if latest_stories:
            for story in latest_stories:
                print(f"Title: {story['title']}")
                print(f"Link: {story['link']}")
                print()
        else:
            print("No stories found or parsing failed.")
    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    main()
