def helpdocs(whichclass):

    helpdoc = ''

    if whichclass == 111:
        helpdoc = '''Here, you need to enter the name of your website.
        This will be displayed at the top of every page you create. As
        such, I recommend you use a short and memorable name that sums
        up the purpose of the site as a whole, as opposed to a single
        page.'''

    elif whichclass == 999:
        helpdoc = '''Here, you can choose between two possible themes,
        dark or light. The dark theme has a dark background and light
        text, whereas the light theme has a light background and dark
        text. This will be applied to the entire website, including
        features such as the navigation bar at the top. If you’re not
        sure which to use, I recommend starting with the light theme.'''

    elif whichclass == 0:
        helpdoc = '''Here, you need to enter the name of this individual
        page. Unlike the website name you entered earlier, this will
        only be displayed on a single page, underneath the website name.
        It must not be the same as the name of another page you have
        already created in the site.'''

    elif whichclass == 1:
        helpdoc = '''Here, you need to enter the last part of the web
        address of this individual page. This will go in the search bar
        at the top of your browser (e.g. www.example.com/address).
        It must be unique, as any web address can point to one page and
        one page only. It must also contain only letters, numbers, "_",
        and "-", in any combination, so no spaces or special characters
        except the two permitted ones. I recommend making it as similar
        to the page name as possible, as this will make it easier for
        users to navigate the site.'''

    elif whichclass == 2:
        helpdoc = '''Here, you need to enter up to a paragraph of text
        on the current page. If you want to add an image and/or another
        paragraph, you will have the chance to do so after submitting
        the current paragraph.'''

    elif whichclass == 3:
        helpdoc = '''Here, if you choose to add an image, you will then
        have the option to upload one from your computer. You will also
        have to answer questions on its positioning and size, as well as
        entering a description of the image to be used by screen
        readers, in the interest of accessibility.'''

    elif whichclass == 4:
        helpdoc = '''Here, you can upload an image from your computer’s
        file storage. It must be in .jpg, .jpeg, or .png format. It will be
        placed alongside the paragraph that you just uploaded in the
        prior step.'''

    elif whichclass == 5:
        helpdoc = '''Here, you must enter a description of the image you
        just uploaded. This description is not a caption, but something
        called alt-text. If a visually impaired user is accessing your
        site with a screen reader, this description will be what they
        hear. It does not normally show on the screen, so don't worry
        about it affecting the appearance of your site. '''

    elif whichclass == 6:
        helpdoc = '''Here, use the buttons to select the position of the
        image relative to the text in the current section. You can place
        it above the text, below the text, to the left, or to the
        right.'''

    elif whichclass == 7:
        helpdoc = '''Here, use the buttons to choose a size for an
        image. Extra Small has a width of 100 pixels, Small has a width
        of 300 pixels, Medium has a width of 500 pixels, Large has a
        width of 700 pixels, and Extra Large has a width of 900 pixels.
        If you do not want to use any of these exact sizes, choose Auto,
        and the image will retain its current size. Note that the fixed
        sizes automatically update the image's height proportionate to
        its width, so your image will never look distorted.'''

    elif whichclass == 8:
        helpdoc = '''Here, choose whether or not to add a hyperlink to
        the bottom of this section. If you choose to do so, you will
        then be prompted to enter the address of the link, and the
        clickable text.'''

    elif whichclass == 9:
        helpdoc = '''Here, enter the web address to which you want the
        link to point (e.g. example.com). If even one character is off,
        the link will not work or will point to the wrong website, so I
        strongly recommend copy-pasting it.'''

    elif whichclass == 10:
        helpdoc = '''Here, enter the text you want displayed on screen
        for the user to click (e.g. "My social media account").'''

    elif whichclass == 11:
        helpdoc = '''Here, you can choose to add a new paragraph to your
        website. If you choose to do so, you will repeat the previous
        steps (adding text, and an image and a link if desired), before
        being given a chance to add yet another paragraph, or proceed to
        the next step if you are done with the current page.'''

    elif whichclass == 12:
        helpdoc = '''Here, you can choose whether or not to add a link
        to the page you just created to your website’s navigation bar.
        Like the website name and theme you chose at the beginning of
        the session, the navigation bar stays the same regardless of the
        page you are currently viewing. Once you have completed this
        step, you will be able to view your finished page.'''

    else:
        helpdoc = '''An error has occured. This page is intended to be
        accessed only from the chat interface, by pressing on a help
        link.'''

    return helpdoc
