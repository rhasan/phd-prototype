class LoginAreaNavigation():

    def __init__(self, href, caption):
        self.href = href
        self.caption = caption

def get_login_navigation(user):
    
    if not user:        
        login_link = LoginAreaNavigation(href = '/login', caption = 'login')
        navigation_links.append(login_link)

    else:
        (user_id,age,gender,occupation,zip_code) = user
        navigation_links = list()
        home_link = LoginAreaNavigation(href = '/home', caption = 'Home' )
        navigation_links.append(home_link)
        
        profile_link = LoginAreaNavigation(href = '/profile', caption = 'Profile')
        navigation_links.append(profile_link)

        logout_link = LoginAreaNavigation(href = '/logout' , caption = user_id + '(logout)')
        navigation_links.append(logout_link)

                
    return navigation_links
