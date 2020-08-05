class TagFormatter:
    """
    Шаблоны для форматирования тегов целевого узла
    """

    @staticmethod
    def of(tag_name):
        if tag_name in dir(TagFormatter):
            return getattr(TagFormatter, tag_name)

        return TagFormatter.p

    @staticmethod
    def p(elem, soup):
        TagFormatter._br(elem, soup)

    @staticmethod
    def a(elem, _):
        if elem.attrs.get('href') is not None:
            elem.replace_with('{} [{}]'.format(elem.text.strip(), elem.attrs['href']))
        else:
            elem.replace_with(elem.text)

    @staticmethod
    def h(elem, soup):
        TagFormatter._br(elem, soup)

    h1 = h2 = h3 = h4 = h5 = h6 = h

    @staticmethod
    def _br(elem, soup):
        elem.insert_after(soup.new_tag('br'))
        elem.insert_after(soup.new_tag('br'))
