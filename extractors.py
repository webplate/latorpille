from htmldom import htmldom

def find_attr(dom, selector, attribute):
    out = dom.find(selector).first()
    if out != None:
        out = out.attr(attribute)
    return out

def crop(doc, start='', end=''):
    """keep part of doc between start and end"""
    cropped = doc[doc.find(start)+len(start):]
    endi = cropped.find(end)
    if endi != 0:
        cropped = cropped[:cropped.find(end)]
    if len(cropped) > 0:
        # and remove spaces
        forbidden = [' ', '\n', '\t']
        while cropped[0] in forbidden:
            cropped = cropped[1:]
        while cropped[-1] in forbidden:
            cropped = cropped[:-1]
    return cropped
    
def find_crop(dom, selector, start, end):
    out = dom.find(selector).first()
    if out != None:
        out = out.html()
        out = crop(out, start, end)
    return out

def find_crop_last(dom, selector, start, end):
    #~ out = dom.find(selector).last()
    out = dom.find(selector)
    if out != None:
        out = out.html()
        out = crop(out, start, end)
    return out

def is_url(text):
    """check if we have received an actual URL
    TODO: and no malicious code"""
    if text.startswith('http://') or text.startswith('https://'):
        return True
    else:
        return False

def find_provider(url, providers):
    for p in providers:
        for purl in p['domains']:
            if url.startswith(purl):
                return p, purl
    return None, None

def find_from_rule(rule, dom):
    info = None
    # use a specified function in the rule
    if not isinstance(rule[0], str):
        func = rule[0]
        args = rule[1:]
        info = func(dom, *args)
    # special syntax for commonly used extraction functions
    elif len(rule) == 3:
        info = find_crop(dom, rule[0], rule[1], rule[2])
    elif len(rule) == 2:
        info = find_attr(dom, rule[0], rule[1])
    return info

def extract_profile(url, providers):
    """use htmldom to extract information from page
    use different rules for different websites"""
    provider, domain = find_provider(url, providers)
    if provider != None:
        cropped_url = crop(url, domain)
        dom = htmldom.HtmlDom(url)
        try:
            dom = dom.createDom()
        except Exception:
            return None
        
        # check if we are on profile url or search for one:
        purls = provider['profile_urls']
        for u in purls:
            if cropped_url.startswith(u):
                # extract
                out = {'profile_url': url,
                        'domain': domain}
                for key in provider['extract_rules']:
                    rule = provider['extract_rules'][key]
                    info = find_from_rule(rule, dom)
                    if info != None:
                        out.update({ key: info})
                return out
        
        # redirect to profilepage (recursive)
        for crawl in provider['crawl_rules']:
            if cropped_url.startswith(crawl[0]):
                next_url = find_from_rule(crawl[1], dom)
                if next_url != None:
                    return extract_profile(domain + next_url, providers)
                
    return None

providers = [
    {'domains': ['https://www.blablacar.fr'],
    'profile_urls': ['/membre/profil/'],
    'crawl_rules': [('/trajet-', ('.MemberCard-name a', 'href'))],
    'extract_rules': {
        'name': ('ul.main-infos-list h1', '<h1>', '<span class='),
        'age': ('ul.main-infos-list span.user-age', '(', 'ans)'),
        'description': ('.member-bio p', '<p>', '</p>'),
        'photo_url': ('.member-picture img', 'src'),
        'inscription_date': (find_crop_last, '.main-column-list li', 'Date d\'inscription : ', '</li>')
        }
    },
    {'domains': ['https://www.blablacar.it'],
    'profile_urls': ['/utente/visualizza/'],
    'crawl_rules': [('/passaggio-', ('.MemberCard-name a', 'href'))],
    'extract_rules': {
        'name': ('ul.main-infos-list h1', '<h1>', '<span class='),
        'age': ('ul.main-infos-list span.user-age', '(', 'anni)'),
        'description': ('.member-bio p', '<p>', '</p>'),
        'photo_url': ('.member-picture img', 'src'),
        'inscription_date': (find_crop_last, '.main-column-list li', 'Data d\'iscrizione:', '</li>')
        }
    }
]


if __name__ == '__main__':
    #~ url = "https://www.blablacar.fr/membre/profil/YZuqUY0z1WIqfm8xBCj7hQ"
    #~ url = "https://www.blablacar.it/utente/visualizza/EjSwRuLOG69GXfzI-PGINw"
    #~ url = "https://www.blablacar.fr/trajet-paris-lyon-293845851"
    #~ url = "https://www.blablacar.it/passaggio-milano-roma-303542203" #NOT WORKING!!??
    url = "https://www.blablacar.it/passaggio-milano-roma-307897569"
    from pprint import pprint 
    pprint(extract_profile(url, providers))
