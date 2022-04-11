import random

xing_str = '赵 钱 孙 李 周 吴 郑 王 陈 褚 卫 蒋 沈 韩 杨 朱 秦 尤 许 何 吕 施 张 孔 曹 严 华 金 魏 陶 姜 戚 谢 邹 喻 柏 水 窦 章 云 苏 潘 葛 奚 范 彭 郎'
ming_str = '大 二 叁 四 伍 陆 七 八 九'
add_score_things = '点赞 赞美 打电话 帮助 送礼'
reduce_score_things = '打架 吵架 欺骗 造谣'


names = []
records = []  # 各个用户之间的关系


def mock_names():
    xings = xing_str.split(' ')
    mings = ming_str.split(' ')
    for i in range(1000):
        xing = random.choice(xings)
        ming = random.choice(mings)
        names.append((i+1, xing+ming))


def mock_records():
    good_things = add_score_things.split(' ')
    bad_things = reduce_score_things.split(' ')
    things = good_things+bad_things
    for i in range(5000):
        n1 = random.choice(names)
        n2 = random.choice(names)
        while(n1 == n2):
            n2 = random.choice(names)
        thing = random.choice(things)
        if(things.index(thing) >= len(good_things)):
            score = -1
        else:
            score = 1
        records.append((n1, thing, n2, score))


def mock_data():
    mock_names()
    mock_records()


mock_data()