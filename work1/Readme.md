五十多万封邮件被平均放入了五个文件夹中（a_d，e_j，k_p，q_s，t_z）。建立索引时，按顺序执行build_index.py，normalize.py，merge_file.py，需要注意修改文件的路径。查询时，执行quiry.py。

**temp/df_a_d.json**
记录了邮件总目录dir里面，以a/b/c/d开头的文件夹中的邮件。
df文件中以键值对的形式，保存了单词以及相应的词频。

**temp/dict_a_d.json**
记录了邮件总目录dir里面，以a/b/c/d开头的文件夹中的邮件。
dict文件中以键值对的形式，key：单词，value：多个元组，
每个元组中第一位保存文章id，第二位保存这篇文章中该单词的词频。

**temp/id_a_d.json**
记录了邮件总目录dir里面，以a/b/c/d开头的文件夹中的邮件。
id文件以键值对的形式，存储邮件路径及邮件id。

**temp/tf_a_d.json**
记录了邮件总目录dir里面，以a/b/c/d开头的文件夹中的邮件。
对dict文件的进一步处理，计算每个文章向量的长度，对tf进行归一化。
结果存入tf文件中。

**TF_beforeD、TF_EtoJ、TF_KtoP、TF_QtoS、TF_TtoZ**是按照首字母排序的单词-文章ID-tf数据。
**DF.json**是单词-文档频率数据。
**ID.json**是文章ID-路径数据。

