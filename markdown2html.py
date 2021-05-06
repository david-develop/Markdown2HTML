#!/usr/bin/python3
"""Takes an argument 2 strings both files and verify errors"""
import sys
import os.path


if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    if not os.path.isfile(arguments[1]):
        sys.stderr.write("Missing {}\n".format(arguments[1]))
        exit(1)

    readme_file = arguments[1]
    output_file = arguments[2]

    def count_numchar(string, spec_char):
        """
        Function that count the begining's chararcters repeated
        Return: number of #
        """
        count = 0
        if string[0] == spec_char:
            for char in string:
                if char == spec_char:
                    count += 1
                else:
                    break
        return count

    with open(readme_file, encoding="utf-8") as f:
        all_txt = f.read()
        all_txt_list = all_txt.split('\n')
        final_txt = ''
        print(all_txt_list)
        for idx, line in enumerate(all_txt_list):

            if line != '' and line[0] == '#':
                count = count_numchar(line, '#')
                if count > 0:
                    line = line.lstrip('#')
                    html_tag_b = '<h{}>'.format(count)
                    html_tag_e = '</h{}>'.format(count)

                    result_line = html_tag_b + line.strip() + html_tag_e + '\n'
                    final_txt += result_line
                else:
                    final_txt += line

            elif line != '' and line[0] == '-':
                if (all_txt_list[idx - 1] and all_txt_list[idx - 1][0] != '-')\
                    or (all_txt_list[idx - 1] == '' and
                        all_txt_list[idx - 1] is not None) or\
                        idx == 0:
                    final_txt += '<ul>\n'

                html_tag_b = '<li>'
                html_tag_e = '</li>'
                line = line.lstrip('-')

                result_line = html_tag_b + line.strip() + html_tag_e + '\n'
                final_txt += result_line

                try:
                    if all_txt_list[idx + 1][0] != '-':
                        final_txt += '</ul>\n'
                except IndexError:
                    final_txt += '</ul>\n'

            elif line == '':
                final_txt += '\n'

    with open(output_file, 'w') as f:
        f.write(final_txt)
