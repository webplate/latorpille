import extractors

def test_crop():
    assert extractors.crop("", "", "") == ""
    assert extractors.crop("allo test allu", "allo", "allu") == "test"
    assert extractors.crop("allo\n \t \n allu", "allo", "allu") == ""
    assert extractors.crop("fgjaga$/é@à&%%(&/allo\n \tbinz \n allu&%òì$(%/)(%", "allo", "allu") == "binz"
    
def test_extract_profile():

    #~ url = "https://www.blablacar.it/passaggio-milano-roma-303542203" #NOT WORKING!!??
    #~ url = "https://www.blablacar.it/passaggio-milano-roma-307897569"
    #~ url = "https://www.airbnb.com/users/show/9993714"
    #~ url = "https://www.airbnb.com/rooms/1930715?checkin=11%2F17%2F2015&checkout=11%2F18%2F2015&s=PYHhKEvX"
    #~ url = "https://www.airbnb.com/rooms/8324971?checkin=11%2F17%2F2015&checkout=11%2F18%2F2015&s=PYHhKEvX"
    #~ url = "https://www.airbnb.fr/rooms/73128?s=QkSTTUX4#host-profile"
    
    #Test blablacar fr user page full extraction
    url = "https://www.blablacar.fr/membre/profil/YZuqUY0z1WIqfm8xBCj7hQ"
    result = {'age': '63',
     'description': '"Informaticien encore en activité.\r\n'
                    'J&#039;aime bien discuter et voyager."',
     'domain': 'https://www.blablacar.fr',
     'inscription_date': '23 mai 2014',
     'name': 'Serge L',
     'photo_url': 'https://d2kwny77wxvuie.cloudfront.net/user/ppkaW8_HTuCvUq5u89HV_A/thumbnail_144x144.jpeg',
     'profile_url': 'https://www.blablacar.fr/membre/profil/YZuqUY0z1WIqfm8xBCj7hQ'}
    extraction = extractors.extract_profile(url, extractors.PROVIDERS)
    assert len(extraction) == len(result)
    for key in result:
        assert extraction[key] == result[key]
    
    #Test blablacar redirection from travel to user page
    url = "https://www.blablacar.fr/trajet-evry-lyon-330634122?tracked_feature=top-trips"
    extraction = extractors.extract_profile(url, extractors.PROVIDERS)
    assert extraction['name'] == 'Marine G'
    
    #Test blabla it
    url = "https://www.blablacar.it/utente/visualizza/EjSwRuLOG69GXfzI-PGINw"
    extraction = extractors.extract_profile(url, extractors.PROVIDERS)
    assert extraction['name'] == 'Davide D'
 
    #Test airbnb
    url = "https://www.airbnb.com/users/show/9993714"
    extraction = extractors.extract_profile(url, extractors.PROVIDERS)
    assert extraction['name'] == 'Sonya &amp; Gabriel'
    
    

