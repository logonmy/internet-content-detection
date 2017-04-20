import sys
sys.path.append('../../')

import base.base_parser as base_parser
import init
import utils.tools as tools
from utils.log import log
import base.constance as Constance

# 必须定义 网站id
SITE_ID = 12
# 必须定义 网站名
NAME = 'luzhougaozhong'


# 必须定义 添加网站信息
@tools.run_safe_model(__name__)
def add_site_info():
    log.debug('添加网站信息')
    site_id = SITE_ID
    name = NAME
    table = 'Op_site_info'
    url = "http://www.lugao.net/"

    base_parser.add_website_info(table, site_id, url, name)

# 必须定义 添加根url
@tools.run_safe_model(__name__)
def add_root_url(parser_params = {}):
    log.debug('''
        添加根url
        parser_params : %s
        '''%str(parser_params))

    url = "http://www.lugao.net/"
    html, request = tools.get_html_by_requests(url)
    urls = tools.get_urls(html)
    for url in urls:
        base_parser.add_url('op_urls', SITE_ID, url)

# 必须定义 解析网址
def parser(url_info):
    url_info['_id'] = str(url_info['_id'])
    log.debug('处理 \n' + tools.dumps_json(url_info))

    source_url = url_info['url']
    depth = url_info['depth']
    website_id = url_info['site_id']
    description = url_info['remark']

    html = tools.get_html_by_urllib(source_url)
    if html == None:
        base_parser.update_url('Op_urls', source_url, Constance.EXCEPTION)
        return

    # 判断中英文
    regex = '[\u4e00-\u9fa5]+'
    chinese_word = tools.get_info(html, regex)
    if not chinese_word:
        base_parser.update_url('Op_urls', source_url, Constance.EXCEPTION)
        return
    urls = tools.get_urls(html)

    urls = tools.fit_url(urls, "lugao")
    for url in urls:
        base_parser.add_url('Op_urls', website_id, url, depth + 1)


    # 取当前页的文章信息
    # 标题

    regexs = '<title>(.*?)</title>'
    title = tools.get_info(html, regexs)
    title = title and title[0] or ''
    title = tools.del_html_tag(title)

    #时间
    regexs = '发表时间：(.*?)&nbsp;'
    release_time = tools.get_info(html, regexs)
    release_time = release_time and release_time[0] or ''
    release_time = tools.del_html_tag(release_time)

    #作者
    author = '编辑：(.*?)</div>'
    author = tools.get_info(html, regexs)
    author = release_time and author[0] or ''
    author = tools.del_html_tag(author)

    #文章来源
    regexs = '来源：(.*?)&nbsp'
    origin = tools.get_info(html, regexs)
    origin = origin and origin[0] or ''
    origin = tools.del_html_tag(origin)

    #点击数
    regexs = '评论：<span class="style1">(\d*?)</span>'
    watched_count = tools.get_info(html, regexs)
    watched_count = watched_count and watched_count[0] or ''
    watched_count = tools.del_html_tag(watched_count)

    # 内容
    regexs = ['<td height="2" class="graphic10">(.*?)来源']
    content = tools.get_info(html, regexs)
    content = content and content[0] or ''
    content = tools.del_html_tag(content)

    log.debug('''
                depth               = %s
                title               = %s
                release_time        = %s
                author              = %s
                origin              = %s
                watched_count       = %s
                content             = %s
             ''' % (depth, title, release_time, author, origin, watched_count, content))

    if content and title:
        base_parser.add_op_info('Op_content_info', website_id, title=title, release_time=release_time, author=author,
                                origin=origin, watched_count=watched_count, content=content)

    # 更新source_url为done
    base_parser.update_url('op_urls', source_url, Constance.DONE)

    # # 解析
    # html, request = tools.get_html_by_requests(root_url)
    # if not html:
    #     base_parser.update_url('urls', root_url, Constance.EXCEPTION)
if __name__ == '__main__':
    url = "http://www.lugao.net/article.aspx?id=3473"
    html, request = tools.get_html_by_requests(url)
    regexs = ['<td height="2" class="graphic10">(.*?)来源']
    content = tools.get_info(html, regexs)
    content = content and content[0] or ''
    content = tools.del_html_tag(content)
    print(content)
    #urls = tools.get_urls(html)
    #print(urls)
    # for url in urls:
    #     print(url)
        #base_parser.add_url('article_urls', SITE_ID, url)





