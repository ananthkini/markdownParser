
import re
import sys
import collections




def paragraph(match_obj):
	line = match_obj.group(1)
	trimmed = line.strip()
	if re.search(r'^<\/?(ul|ol|li|h|p|bl)', trimmed):
		return "\n" + line + "\n"
	return "\n<p>{}</p>\n".format(trimmed);

def ul_list(match_obj):
	item = match_obj.group(1);
	return "\n<ul>\n\t<li>{}</li>\n</ul>".format(item.strip());

def ol_list(match_obj):
	item = match_obj.group(1);
	return "\n<ol>\n\t<li>{}</li>\n</ol>".format(item.strip());

def blockquote(match_obj):
	item = match_obj.group(2);
	return "\n<blockquote>{}</blockquote>".format(item.strip());

def header(match_obj):
	level = len(match_obj.group(1))
	title = match_obj.group(2).strip()
	return '<h{0}>{1}</h{0}>'.format(level, title)




rules = collections.OrderedDict()
rules[r'(#+)(.*)\s'] = header # headers
rules[r'\[([^\[]+)\]\(([^\)]+)\)\s'] = r'<a href="\2">\1</a>' # links
rules[r'(\*\*|__)(.*?)\1\s'] = r'<strong>\2</strong>' # bold
rules[r'(\*|_)(.*?)\1'] = r'<em>\2</em>' # emphasis
rules[r'\~\~(.*?)\~\~'] = r'<del>\1</del>' # del
rules[r'\:\"(.*?)\"\:'] = r'<q>\1</q>' # quote
rules[r'`(.*?)`'] = r'<code>\1</code>' # inline code
rules[r'\n\*(.*)'] = ul_list # ul lists
rules[r'\n[0-9]+\.(.*)'] = ol_list # ol lists
rules[r'\n(&gt;|\>)(.*)'] = blockquote # blockquotes
rules[r'\n-{5,}'] = r"\n<hr />" # horizontal rule
rules[r'\n([^\n]+)\s\n'] = paragraph # add paragraphs
rules[r'<\/ul>\s?<ul>\s'] = r'' # fix extra ul
rules[r'<\/ol>\s?<ol>\s'] = r'' # fix extra ol
rules[r'<\/blockquote><blockquote>'] = r"\n" # fix extra blockquote




def render(text):
	text = '\n' + text + '\n'
	for regex, replacement in rules.items():
		text = re.sub(regex, replacement, text)
	return text.strip()



if __name__ == '__main__':
	input_text = sys.stdin.read()
	rendered_text = render(input_text)
print(rendered_text)