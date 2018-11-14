import re
import jieba

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def check_length(fdirs):
    for fdir in fdirs:
        fin = open(fdir, 'r', encoding='utf-8')
        print(fdir, ': ', len(fin.readlines()))
        fin.close()


def _clean_sentence(sent):
    # sent = re.sub(u"[^\u4E00-\u9FFF\！\，\。\？]+", '', sent)
    sent = sent.lower()
    filtrate = re.compile(u'[^\u4E00-\u9FA5\a-z]')  # non-Chinese unicode range
    context = filtrate.sub(r'', sent)  # remove all non-Chinese characters

    return context


def char_base_parsing(fdir, outp_dir):
    num_files = 0
    
    fout = open(outp_dir, 'w', encoding='utf-8')
    with open(fdir, 'r', encoding='utf-8') as f:
        num_files = 0
        for line in f.readlines():
            print(line)
            line = _clean_sentence(line)
            line = ' '.join(line)
            
            fout.write(line.strip() + '\n')
            print(line)
            num_files += 1
    fout.close()
    print("processed {} files in {}".format(num_files, fdir))


def word_base_parsing(fdir, outp_dir):
    num_files = 0
    jieba.load_userdict('./hk_words/actor_names.txt')
    jieba.load_userdict('./hk_words/dict.txt.big.txt')

    fout = open(outp_dir, 'w', encoding='utf-8')
    with open(fdir, 'r', encoding='utf-8') as f:
        num_files = 0
        for line in f.readlines():
            # print(line)
            line = _clean_sentence(line)
            stopwords = stopwordslist('./hk_words/stopwords_traditionalChinese.txt')
            outstr = ""
            for word in line:
                if word not in stopwords:
                    outstr += word
            line = ' '.join(jieba.cut(outstr, cut_all=False))
            fout.write(line.strip() + '\n')
            num_files += 1

    fout.close()
    print("processed {} files in {}".format(num_files, fdir))



if __name__ == '__main__':
    
    fs = ['./test_content{}', './test_title{}']
    f_check = []
    
    for f in fs:
        char_base_parsing(f.format('.txt'), f.format('_char.txt'))
        word_base_parsing(f.format('.txt'), f.format('_word.txt'))
    
    # check_length([fin1, fin2, fout1, fout2, fout3, fout4])

