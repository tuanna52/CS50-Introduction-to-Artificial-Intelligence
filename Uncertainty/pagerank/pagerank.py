import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    trans_mod = dict()

    # Number of page
    N = len(corpus)

    # Number of links of the current page
    num_links = len(corpus[page])
    for link in corpus[page]:
        if (link == page) and (num_links == 1):    #Check if current page contains only one link to itself
            num_links = num_links - 1

    if num_links != 0:    #check if current page has links
        for cor in corpus:
            if cor == page:
                trans_mod[cor] = (1-damping_factor)/N
            elif cor not in corpus[page]:
                trans_mod[cor] = (1-damping_factor)/N
            else:
                trans_mod[cor] = (1-damping_factor)/N + damping_factor/num_links
    else:   #check if current page has no link
        for cor in corpus:
            trans_mod[cor] = 1/N

    return trans_mod

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()

    for cor in corpus:
        pagerank[cor] = 0

    cur_page = random.choice(list(corpus.keys()))
    trans_model = transition_model(corpus, cur_page, damping_factor)
    pagerank[cur_page] += 1

    for _ in range(1, n):
        cur_page = random.choices(list(trans_model.keys()), list(trans_model.values()))[0]
        pagerank[cur_page] += 1
        trans_model = transition_model(corpus, cur_page, damping_factor)

    #Normalizing so that the results sum to 1
    norm_opt = 1/sum(pagerank.values())
    pagerank.update((x, y*norm_opt) for x, y in pagerank.items())

    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    icorpus = dict()
    pagerank_past = dict()

    # Number of page
    N = len(corpus)

    for cor in corpus:
        temp = 1/len(corpus)
        pagerank[cor] = temp
        pagerank_past[cor] = temp
        pages_link_to = set()
        for k, v in corpus.items():
            if cor in v:
                pages_link_to.add(k)
        icorpus.update({cor:pages_link_to})
    
    check = 0
    while check < len(icorpus):
        check = 0

        for icor in icorpus:
            temp = 0
            if  len(icorpus[icor]) == 0:
                temp = (1-damping_factor)/N
            else:
                temp = (1-damping_factor)/N
                for i in icorpus[icor]:
                    num_links_i = len(corpus[i])
                    if num_links_i != 0:
                        temp = temp + damping_factor*pagerank[i]/num_links_i
                    else:
                        temp = temp + damping_factor*pagerank[i]/N

            if abs(temp-pagerank[icor]) < 0.001:
                check+=1
            
            pagerank[icor] = temp

    #Normalizing so that the results sum to 1
    norm_opt = 1/sum(pagerank.values())
    pagerank.update((x, y*norm_opt) for x, y in pagerank.items())    

    return pagerank


if __name__ == "__main__":
    main()

