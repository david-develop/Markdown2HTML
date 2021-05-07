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
        txt_list = all_txt.split('\n')
        final_txt = ''

        for idx, line in enumerate(txt_list):
            spe_char_list = ['#', '-', '*']

            if line != '':
                first_char = line[0]
                if first_char == '#':
                    count = count_numchar(line, '#')
                    if count > 0:
                        line = line.lstrip('#')
                        html_t_b = '<h{}>'.format(count)
                        html_t_e = '</h{}>'.format(count)

                        html_f = html_t_b + line.strip() + html_t_e + '\n'
                        final_txt += html_f
                    else:
                        final_txt += line

                elif first_char == '-' or first_char == '*':
                    html_list_o = '<ul>' if first_char == '-' else '<ol>'
                    html_list_o_end = '</ul>' if first_char == '-' else '</ol>'

                    if (txt_list[idx - 1] and txt_list[idx - 1][0] !=
                        first_char) or (txt_list[idx - 1] == '' and
                                        txt_list[idx - 1] is not None) or\
                            idx == 0:
                        final_txt += '{}\n'.format(html_list_o)

                    html_t_b = '<li>'
                    html_t_e = '</li>'
                    line = line.lstrip(first_char)

                    html_f = html_t_b + line.strip() + html_t_e + '\n'
                    final_txt += html_f

                    try:
                        if txt_list[idx + 1][0] != first_char:
                            final_txt += '{}\n'.format(html_list_o_end)
                    except IndexError:
                        final_txt += '{}\n'.format(html_list_o_end)

                elif first_char not in spe_char_list:
                    html_list_o = '<p>'
                    html_list_o_end = '</p>'

                    if idx == 0 or (txt_list[idx - 1] == '' and
                                    txt_list[idx - 1] is not None) or\
                            (txt_list[idx - 1] and
                             txt_list[idx - 1][0] in spe_char_list):
                        final_txt += '{}\n'.format(html_list_o)

                    final_txt += line.strip() + '\n'

                    try:
                        if txt_list[idx + 1][0] in spe_char_list:
                            final_txt += '{}\n'.format(html_list_o_end)
                    except IndexError:
                        final_txt += '{}\n'.format(html_list_o_end)

            else:
                final_txt += '\n'

    with open(output_file, 'w') as f:
        f.write(final_txt)
