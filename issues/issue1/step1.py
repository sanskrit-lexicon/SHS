import re
import os

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines() if line.strip()]

    lextags_with_paren = ['mfn\\.', 'mn\\.', 'mf\\.', 'nf\\.', 'adv\\.', 'subst\\.', 'adj\\.', 'sub\\.', 'pron\\.',
               'm\\.', 'f\\.', 'n\\.', 'ind\\.']
    tag_pattern = re.compile(r'((?:' + '|'.join(lextags_with_paren) + r'))\s*(\({#.*?#}\))')

    lextags_standalone = ['mfn\\.', 'mn\\.', 'mf\\.', 'nf\\.', 'adv\\.', 'subst\\.', 'adj\\.', 'sub\\.', 'pron\\.',
               'm\\.', 'f\\.', 'n\\.', 'ind\\.', 'r\\.', 'fn\\.', 'Subst\\.', 'subst\\.']
    standalone_pattern = re.compile(r'(?:^|(?<=\s)|(?<=¦))(' + '|'.join(lextags_standalone) + r')(?=\s|$)')

    # Split at '¦', putting '¦' at the beginning of the next line (with a space before the lex tag or text, as per expected output: "¦ <lex>m.</lex> ({#-SaH#})")
    output_lines = []
    for line in lines:
        if '¦' in line:
            parts = line.split('¦', 1)
            before = parts[0]
            after = parts[1]
            if after.strip():
                output_lines.append(before)
                output_lines.append('¦ ' + after.strip())
            else:
                output_lines.append(line)
        else:
            output_lines.append(line)

    temp_lines = []
    for line in output_lines:
        r_sub = re.sub(r'(?:^|(?<= ))r\.\s*', '<lex>r.</lex> ', line)
        idx = r_sub.find('<lex>r.</lex> ')
        if idx > 0:
            part_before = r_sub[:idx].rstrip()
            part_after = r_sub[idx:]
            if part_before:
                temp_lines.append(part_before)
            temp_lines.append(part_after)
        else:
            temp_lines.append(r_sub)

    ab_tags = ['intensitive v.', 'Aptote noun.', 'frequent. v.', 'intents. v.', 'passive v.', 'nominal v.', 'reiter. v.', 'intens. v.', 'causal v.', 'desid. v.', 'v. redup.', 'pass. v.', 'reit. v.', 'freq. v.', 'adverb.', 'aptote.', 'deprec.', 'nom. v.', 'Aptote.', 'metaph.', 'ut sup.', 'ut inf.', 'desid.', 'liter.', 'deriv.', 'Desid.', 'e. g.', 'N. W.', 'q. v.', 'A. D.', 'plur.', 'N. E.', 'S. W.', 'inst.', 'caus.', 'Sept.', 'Plur.', 'i. e.', 'comp.', 'priv.', 'pass.', 'sing.', 'affs.', 'Caus.', 'avds.', 'Sing.', 'Phil.', 'Accu.', 'pres.', 'masc.', 'S. E.', 'Plu.', 'Mss.', 'etc.', 'abl.', 'loc.', 'rep.', 'lit.', 'viz.', 'Dec.', 'dat.', 'mas.', 'Nov.', 'dim.', 'der.', 'Atm.', 'Oct.', 'nom.', 'aug.', 'neg.', 'fig.', 'gen.', 'grs.', 'fem.', 'cls.', 'Jan.', 'int.', 'aff.', 'Par.', 'plu.', 'voc.', 'acc.', 'reg.', 'irr.', 'inf.', 'op.', 'pl.', 'du.', 'Pl.', 'Du.', 'cl.', '&c.', 'pp.', 'Ex.', 'M.', 'E.']
    ab_tags.sort(key=len, reverse=True)
    ab_pattern = re.compile(r'(?:^|(?<=[\s(]))(' + '|'.join(re.escape(tag) for tag in ab_tags) + r')(?=[\s,;.)]|$|[,;\.])')

    input_dir = os.path.dirname(input_path)
    
    bot_tags_path = os.path.join(input_dir, 'bot_tags.txt')
    if os.path.exists(bot_tags_path):
        with open(bot_tags_path, 'r', encoding='utf-8') as bf:
            bot_tags = [line.split('\t')[0].strip() for line in bf if line.strip()]
        bot_tags.sort(key=len, reverse=True)
        bot_pattern = re.compile(r'(^|[\s(])(' + '|'.join(re.escape(tag) for tag in bot_tags) + r')(?=[\s,;.)]|$)')
    else:
        bot_tags = []
        bot_pattern = None

    zoo_tags_path = os.path.join(input_dir, 'zoo_tags.txt')
    if os.path.exists(zoo_tags_path):
        with open(zoo_tags_path, 'r', encoding='utf-8') as zf:
            zoo_tags = [line.split('\t')[0].strip() for line in zf if line.strip()]
        zoo_tags.sort(key=len, reverse=True)
        zoo_pattern = re.compile(r'(^|[\s(])(' + '|'.join(re.escape(tag) for tag in zoo_tags) + r')(?=[\s,;.)]|$)')
    else:
        zoo_tags = []
        zoo_pattern = None

    processed = []
    for line in temp_lines:
        result = tag_pattern.sub(r'<lex>\1</lex> \2\n', line)
        result = standalone_pattern.sub(r'<lex>\1</lex>\n', result)
        
        # Replace .E. with a newline and <ab>E.</ab>\n so it starts on a new line (as per expected output)
        result = result.replace('.E.', '\n<ab>E.</ab>\n')

        # Apply <ab> tags using the single compiled regex
        result = ab_pattern.sub(r'<ab>\g<1></ab>', result)
        
        # Apply <bot> and <zoo> tags (only if the tag files were present)
        if bot_pattern is not None:
            result = bot_pattern.sub(r'\1<bot>\2</bot>', result)
        if zoo_pattern is not None:
            result = zoo_pattern.sub(r'\1<zoo>\2</zoo>', result)
        
        # Fix any double-wrapped tags
        result = result.replace('<ab><ab>', '<ab>').replace('</ab></ab>', '</ab>')
        result = result.replace('<bot><bot>', '<bot>').replace('</bot></bot>', '</bot>')
        result = result.replace('<zoo><zoo>', '<zoo>').replace('</zoo></zoo>', '</zoo>')

        r_with_content = re.search(r'<lex>r\.</lex>.*?(\({#.*?#}\))', result)
        if r_with_content:
            end_pos = r_with_content.end(1)
            before_paren_end = result[:end_pos]
            after_paren_end = result[end_pos:]
            result = before_paren_end + '\n' + after_paren_end

        # Put <lex> tags that appear mid-line onto their own line
        result = re.sub(r'(?<=[^ \n])\s+(<lex>)', r'\n\1', result)

        processed.append(result)

    flat_lines = []
    for line in processed:
        flat_lines.extend([l for l in line.split('\n')])

    flat_lines = [line.strip() for line in flat_lines if line.strip()]

    final_lines = []

    def starts_new_block(line):
        # Senses like "1.", "2." should always start on a new line.
        if re.match(r'^\d+\.', line):
            return True
        return (line.startswith('<L>') or
                line.startswith('<LEND>') or
                line.startswith(' <lex>') or
                line.startswith(' <ab>') or
                line.startswith('<lex>') or
                line.startswith('<ab>') or
                line.startswith('¦') or
                (line.startswith('{#') and '¦' in line) or
                line.startswith('.²'))

    def should_not_merge(line, prev_line):
        # Do not merge if the previous line contains <L> or is a closing LEND tag
        if prev_line.strip().startswith('<L>') or prev_line.strip().startswith('<LEND>'):
            return True
        # Do not merge if prev_line is '¦' itself. But in flat_lines, '¦' starts with '<lex>' or text inside output_lines split logic.
        # However, let's keep ¦ and subsequent lex tags merged together.
        if prev_line.strip() == '¦':
            return False
        return (prev_line.rstrip().endswith(')') or
                prev_line.rstrip().endswith('</lex>') or
                prev_line.rstrip().endswith('</ab>'))

    for i, line in enumerate(flat_lines):
        if i > 0 and not starts_new_block(line) and not should_not_merge(line, final_lines[-1]):
            # If the current line is a regular sentence/continuation, merge it.
            # But let's check if the current line starts a new sense mid-line or similar.
            final_lines[-1] = final_lines[-1] + ' ' + line
        elif i > 0 and line.startswith('<lex>') and final_lines[-1] == '¦':
            # Explicitly merge lex tag with a leading '¦' line
            final_lines[-1] = final_lines[-1] + ' ' + line
        else:
            final_lines.append(line)

    # Let's perform a post-processing pass to break numbered senses (e.g., " 2. ") and ".E." onto new lines if they were merged.
    # Also, we want to split a merged sentence like "1. A share or portion. 2. A part. 3. ..." into individual lines.
    split_lines = []
    for line in final_lines:
        if line.startswith('<L>') or line.startswith('<LEND>'):
            split_lines.append(line)
            continue
        
        # Split numbered senses that are inline (e.g., "1. foo 2. bar" -> "1. foo", "2. bar")
        # We find instances of " \d+\. " (with a space before, and a number and dot)
        parts = re.split(r'\s+(?=\d+\.)', line)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Also handle any mid-line etymology .E. or <ab>E.</ab>
            if '<ab>E.</ab>' in part:
                if part.startswith('<ab>E.</ab>'):
                    split_lines.append('<ab>E.</ab>')
                    after_e = part[len('<ab>E.</ab>'):].strip()
                    if after_e:
                        split_lines.append(after_e)
                else:
                    subparts = re.split(r'\s*(?=<ab>E\.</ab>)', part)
                    for sp in subparts:
                        sp = sp.strip()
                        if sp == '<ab>E.</ab>':
                            split_lines.append(sp)
                        elif sp.startswith('<ab>E.</ab>'):
                            split_lines.append('<ab>E.</ab>')
                            after_e = sp[len('<ab>E.</ab>'):].strip()
                            if after_e:
                                split_lines.append(after_e)
                        elif sp:
                            split_lines.append(sp)
            else:
                split_lines.append(part)

    final_text = '\n'.join(split_lines)

    # 1. Remove leading spaces
    final_text = re.sub(r'(?m)^[ ]+', '', final_text)
    
    # 2. Ensure .² is preceded by exactly one space, but not at the start of a line
    final_text = final_text.replace('.²', ' .²').replace('  .²', ' .²')
    final_text = re.sub(r'(?m)^ \.²', '.²', final_text)

    # 3. Merge <lex> and ({#...#}) from next line, then add newline
    final_text = re.sub(r'</lex>\s*\n\s*(\({#.*?#}\))\s*', r'</lex> \1\n', final_text)

    # 4. Swap punctuation out of closing tags
    final_text = re.sub(r'([,.])%\}', r'%}\1', final_text)
    final_text = re.sub(r'([,.])#\}', r'#}\1', final_text)

    # 5. Convert standard ASCII single quote (') to modifier apostrophe (ʼ)
    final_text = final_text.replace("'", "ʼ")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_text + '\n')

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'temp_shs_0.txt')
    output_file = os.path.join(script_dir, 'temp_shs_1.txt')
    process_file(input_file, output_file)
