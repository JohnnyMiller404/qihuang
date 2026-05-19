from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta,timezone
import json
import random
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'qihuang-youth-2024-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db = SQLAlchemy(app)

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')
    search_history = db.relationship('SearchHistory', backref='user', lazy=True, cascade='all, delete-orphan')

class Knowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text)
    precautions = db.Column(db.Text)
    suitable_crowd = db.Column(db.String(200))
    season = db.Column(db.String(50))
    video_url = db.Column(db.String(255))
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    favorites = db.relationship('Favorite', backref='knowledge', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='knowledge', lazy=True, cascade='all, delete-orphan')

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    knowledge_id = db.Column(db.Integer, db.ForeignKey('knowledge.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    knowledge_id = db.Column(db.Integer, db.ForeignKey('knowledge.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 登录装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 初始化数据库和示例数据
def init_db():
    with app.app_context():
        db.create_all()
        
        # 检查是否已有数据
        if Knowledge.query.first() is None:
            sample_knowledge = [
                {
                    'title': '八段锦',
                    'category': '传统功法',
                    'content': '八段锦是中国古代传统保健功法，由八节动作组成。包括：双手托天理三焦、左右开弓似射雕、调理脾胃须单举、五劳七伤往后瞧、摇头摆尾去心火、两手攀足固肾腰、攒拳怒目增气力、背后七颠百病消。',
                    'benefits': '调理气血、强身健体、疏通经络、增强免疫力',
                    'precautions': '动作要柔和，呼吸要自然，不可用力过猛',
                    'suitable_crowd': '大学生、办公族、中老年人',
                    'season': '四季皆宜',
                    'video_url': '/static/八段锦.mp4'
                },
                {
                    'title': '五禽戏',
                    'category': '传统功法',
                    'content': '五禽戏是华佗创编的养生功法，模仿虎、鹿、熊、猿、鸟五种动物的动作。虎戏主肝，鹿戏主肾，熊戏主脾，猿戏主心，鸟戏主肺。',
                    'benefits': '平衡阴阳、调和气血、活动筋骨、增强体质',
                    'precautions': '初学者应循序渐进，避免动作过大',
                    'suitable_crowd': '青年学生、亚健康人群',
                    'season': '春夏秋冬'
                },
                {
                    'title': '艾灸养生',
                    'category': '中医疗法',
                    'content': '艾灸是用艾叶制成的艾条、艾柱，点燃后熏烤人体穴位的中医疗法。常用穴位有足三里、关元、气海、神阙等。',
                    'benefits': '温经散寒、行气活血、扶阳固脱、防病保健',
                    'precautions': (
                        '哪些人群不适合艾灸（1）阴虚火旺体质的人：这类人群容易手足心热、口干舌燥、口舌生疮等，在做艾灸时很容易诱发便秘、咽喉肿痛或头痛等上火的症状。（2）高热、局部红肿热痛患者：这类患者也不适合艾灸治疗。（3）糖尿病患者：糖尿病患者的皮肤感觉比较迟钝，艾灸时容易发生烫伤。（4）孕妇：孕妇的腹部和腰骶部也不能进行艾灸。\n\n'
                        '中国中医科学院主任医师 杨金生：艾草燃烧以后除了温热作用以外，还有大量的挥发油，比如焦油，还有一些艾烟燃烧以后的颗粒样物质。一些人吸收以后，会产生呼吸道症状，比如引发哮喘；另外一些人还会导致过敏——皮肤敏感，皮肤瘙痒甚至出皮疹。\n\n'
                        '　　在做艾灸的过程中，处理不当很有可能达不到养生的效果，甚至带来一些隐患。如果自己在家里进行艾灸，一定要注意以下几点。首先，艾灸的温度不是越烫越好，建议以局部皮肤有温热感，皮肤微红的状态为宜。艾灸时间一般情况下根据个人体质情况，每次选2到3个穴位，每个穴位灸10～15分钟即可；新手或体质偏弱者一周2～3次，给身体留恢复窗口。要注意，餐后1小时、睡前2小时内尽量不做高强度灸；天热闷湿时降低时长与温度。还要注意灸后护理，灸后要补200～300ml温水，30分钟内不吹风、不冲凉；出现红肿水疱先冷敷保护，不要挑破。还要注意灸后护理，灸后要补200～300ml温水，30分钟内不吹风、不冲凉；出现红肿水疱先冷敷保护，不要挑破。\n\n'
                        '中国中医科学院针灸医院主任医师 王莹莹：首次艾灸的人，在医生的辨证下来进行，是否适合艾灸，这是第一。第二，适合哪些经络、适合哪些穴位来刺激，这个问题需要专业的医生来指导，所以建议首次艾灸的人要在医生的指导下进行艾灸的自我保健。\n'
                        '除了上述艾灸注意事项，还有一些艾灸误区请绕开。\n'
                        '艾灸包治百病，对吗？\n'
                        '中国中医科学院针灸医院主任医师 王莹莹：这是肯定不对的，艾灸有非常好的保健和医疗作用，但它并不是包治百病，它有它的适宜病证，有些人群、有些病证还是禁忌艾灸的，所以说它不是包治百病的。\n\n'
                        '哪里痛就灸哪里，对吗？\n'
                        '中国中医科学院主任医师 杨金生：大多数情况是对的，但是个别情况还要区别对待。比如说疼痛是感染性引起的，这个地方就不能灸，如果这个部位靠近大血管，靠近心脏的部位，它就不能灸，有些疾病皮肤溃烂的地方不能灸，所以一定要诊断清楚疼痛是什么原因引起的，这样灸才是安全有效的。\n\n'
                        '艾灸时出汗越多，“寒气”排得越干净，对吗？\n'
                        '中国中医科学院主任医师 杨金生：这个想法不完全对，如果艾灸时间过长，灸的温度过高，出现了大汗淋漓、虚脱，会导致出汗电解质丢失，这样不但起不到治病的作用，反而会加重病情，微微出汗，不可大汗。'
                    ),
                    'suitable_crowd': '体质虚寒者、慢性疲劳者',
                    'season': '秋冬季节尤佳'
                },
                {
                    'title': '药膳食疗',
                    'category': '饮食养生',
                    'content': (
                        '药食同源，食物疗法更显温和\n'
                        '　“民以食为天，食以养为先。”早在《黄帝内经》中，就有“五谷为养，五果为助，五畜为益，五菜为充”的记载，这成为“药食同源”的理论基础。而中医药膳的核心理念在于治未病，即通过饮食调养实现“未病先防、既病防变、瘥后防复”。\n'
                        '　　人们常说“春夏养阳”“长夏胜冬”，“冬病夏治”是广为人知的中医药特色疗法。那么，能否以药膳食补助力冬病夏治？\n'
                        '　　中国中医科学院广安门医院食疗营养部主任王宜告诉记者，“冬病”是指那些好发于冬季，或者在冬季病情会加重的疾病，比如支气管炎、哮喘、风湿及类风湿性关节炎、脾胃虚寒等病症。“夏治”则是趁人体阳气旺盛之时，进行辨证施治，以此预防冬病复发或减轻病症。“此时进行膳食调养，就好比借食物之力在身体里点燃火种，既能驱散沉积的寒气，又能为冬季储备能量。”王宜谈道。\n'
                        '　　中医药膳源于“食药两用”“蕴医于食，寓养于膳”，既将药物作为食物，又将食物赋以药用，二者相辅相成。“药膳并非简单的药材与食材混搭，而是凝结着中国古人‘天人合一’的养生哲学。”广东省中医院院长张忠德介绍，中医食疗注重食物的“药性”，通常根据饮食的性味来调节人体的阴阳平衡。\n'
                        '　　不同于“是药三分毒”的用药原则，食物疗法更显温和。枸杞明目、山药补脾、百合润肺……这些日常食材经过科学配比发挥效用，让人们在享受美食的过程中，悄然完成身体的养护。即便稍有偏差，也不会对身体造成剧烈冲击。正如清代名医张锡纯所言，食疗“即不对症，亦无他患”。\n'
                        '　　因此，无论是冬病夏治的季节性调养，还是日常的体质调理，中医药膳都正以独特的方式融入生活，成为守护健康的“无声良医”。\n'
                        '辨证施膳，遵循精准食补原则\n'
                        '　　中医认为“药补不如食补”，随着人们健康意识的增强，中医药膳越来越受到关注与欢迎。那么，是否人人都能食用药膳？药膳选用不当有没有副作用？食用药膳时要注意些什么？\n'
                        '　　“药膳不能完全普及化，并不是所有人都适合吃药膳。”上海中医药大学附属曙光医院传统医学科主任医师傅慧婷坦言，“比如对于儿童群体，就需要谨慎使用药膳干预，现在临床上很多案例都是给孩子‘补过了’。”\n'
                        '　　“药膳不能千篇一律，应注重食材搭配与膳食的多样化，如温寒搭配、补泻搭配、荤素搭配。”山东中医药大学教授郭瑞华认为，针对每个个体的食补更要精准，“虚者补之，实者泻之，追求的是平衡协调”。如果饮食失衡则会产生危害，如老年人常吃粗粮引发营养不良、消化功能紊乱，女性长期吃素导致月经紊乱甚至卵巢功能早衰等。\n'
                        '　　王宜也表示，在食用药膳时，要严格遵循目前国家规定的106种“药食两用”物质的范围，运用“热者寒之，寒者热之”的中医原则，充分发挥其调理价值。\n'
                        '　　然而，无论何种药膳，食物都是根本，药物只是“锦上添花”，并不能改变食物的性质。在傅慧婷看来，“即便往冰激凌里加了中药，也改变不了其寒凉的属性”。\n'
                        '　　“此外，在制作药膳时，除了优先选用‘药食同源’的材料，还要注意药材与食材的搭配需兼顾功效与味道。”傅慧婷提醒，“如果药味盖过了食物的味道，不仅药膳的适口性差，还会影响其养生功效。”\n'
                        '　　当下，以中药材为原料的中式养生茶饮成为年轻人的“新宠”，益生菌、黑芝麻丸、维生素软胶囊等保健品也颇受欢迎。\n'
                        '　　对于市面上的这些养生茶、养生丸，郭瑞华建议，首先要注意其安全性，如有无毒副作用等，其次要看它是否符合自身体质。\n'
                        '　　“若食用了与体质相悖的产品，会适得其反。比如，姜糖适合虚寒体质，菊花茶适合肝火旺者，脾胃寒者长期喝菊花茶易导致胃部不适，而火旺者过量饮用姜茶则可能引发上火。”郭瑞华说。\n\n\n'
                        '三因制宜，解锁专属食疗密码\n'
                        '　　从《黄帝内经》的“五谷为养”到“冬病夏治”的药膳实践，中医药膳不仅是东方智慧的结晶，更体现了千年来中国人“顺天应时”的生活哲学。那么，如何科学选择适合自己的药膳？\n'
                        '　　“对于药膳的选择，我们一般遵循‘三因制宜’的原则，即因时、因地、因人。”王宜表示，“需要结合不同的时节、地域、人群给予个性化的食疗计划。”\n'
                        '　　俗话说，“一方水土养一方人”，由于南北方气候不同，养生需求也不同，对于食材和烹饪方式的选择就存在差异。\n'
                        '　　南方地区夏季漫长且闷热潮湿，因此当地人注重选用清热祛湿、健脾补气的药材。“清热祛湿类的有荷叶、赤小豆、冬瓜等；健脾补气则可选五指毛桃、山药、白术等。”张忠德介绍道。\n'
                        '　　烹调方面，南方多采用煲汤、炖汤、清蒸的方式，追求原汁原味，口感以清润为主。当地餐桌上常见的菜品就是祛暑的药膳，例如冬瓜荷叶炖水鸭、竹蔗茅根马蹄水、粉葛赤小豆鲫鱼汤等。除此之外，广东地区的居民还喜欢用鸡蛋花、木棉花、布渣叶、火炭母等草药煮凉茶喝，也有祛湿避暑的功效。\n'
                        '　　而在北方，由于气候较为寒冷，人们以面食与肉食为主。“这些食物属性温和，主要用于补气祛寒。”张忠德解释说。但需要注意的是，脾胃虚弱的人食用过量肉食和面食，容易造成积食。他建议，可以使用山楂、乌梅、麦芽做成代茶饮来健脾消食。\n'
                        '　　烹饪方面，北方多采用炖、炸、烧等方法，也经常搭配胡椒、花椒、八角等辛香调料祛寒。“这些辛辣的食品相对温燥，可以适当搭配一些酸菜、酸萝卜等酸味食材，既可开胃消食，又能养阴润燥。”张忠德提醒。\n'
                        '　　另外，由于不同年龄的人群脏腑气血的盛衰情况不一样，食养方面也要注意“因人施膳”。儿童、孕产妇和老年人这三个群体要格外注意。\n'
                        '　　儿童常因为肺气不足，引发感冒、鼻炎、哮喘等。张忠德建议，可用五指毛桃、太子参、党参等补益肺气，如太子参牛肉汤就是不错的选择。此外，夏季人们喜欢开空调，儿童易因此患上“人造风寒”，此时可用生姜、紫苏叶、葱白煮水做代茶饮。如果吃了过多冰冷食物导致拉肚子或肚子不舒服，则可用陈皮、生姜煮水来温中祛寒。\n'
                        '　　“季节变化的时节，儿童容易心火肝火旺，会出现烦躁、情绪不好、睡觉不安等症状。”王宜介绍，“可以用麦芽等疏肝，搭配灯芯花、莲子心等煮水煮汤饮用。”\n'
                        '　　孕妇要供应胎儿的生长发育，因此气血相对偏弱。“党参、桑椹子、龙眼肉做成的药膳可以有效补益气血。”张忠德指出。除此之外，脾胃为气血生化之源，因此可用砂仁、白术、陈皮煮汤，不仅健脾补气，还有助于安胎。“月子期间可以用益母草、当归、桃仁等促进恶露排出，同时可用黄酒、米酒、猪脚姜来祛寒养血。”王宜补充道。\n'
                        '　　老年人的脏腑逐渐衰退，容易出现疲倦乏力、腰腿酸痛、夜尿多、睡觉不踏实。王宜说：“党参、芡实、巴戟天、牛大力等做成的药膳就很适合老年人，比如牛大力煮猪骨头汤、党参芡实煮鸡汤。”“而对于容易上火的人群，煲汤的时候还可以加一些沙参来养阴润燥。”在张忠德看来，“补而不燥”“补而不滞”方为佳。\n'
                        '　　一饮一食养正气，一朝一夕筑安康。养生无须繁复，顺应天时、了解己身，寻常三餐亦可温养。这个夏天，我们不妨从一碗温补汤羹开始，在一粥一饭间，于日常烟火中，寻回身心平衡的健康之道。'
                    ),
                    'benefits': '调理体质、预防疾病、延缓衰老、美容养颜',
                    'precautions': '需根据个人体质选择，不可盲目进补',
                    'suitable_crowd': '所有人群',
                    'season': '根据季节调整配方'
                },
                {
                    'title': '太极拳',
                    'category': '传统功法',
                    'content': '太极拳是内外兼修、刚柔相济的中国传统拳术。强调意念引导，以静制动，以柔克刚。包含起势、野马分鬃、白鹤亮翅等经典动作。',
                    'benefits': '增强体质、改善心肺功能、缓解压力、提高平衡能力',
                    'precautions': '膝关节要放松，不可过度下蹲',
                    'suitable_crowd': '学生、白领、老年人',
                    'season': '全年适宜'
                },
                {
                    'title': '刮痧疗法',
                    'category': '中医疗法',
                    'content': '刮痧是用刮痧板蘸刮痧油反复刮动、摩擦患者皮肤，以治疗疾病的方法。可疏通经络、活血化瘀。',
                    'benefits': '祛风散寒、疏通经络、调和气血、排毒养颜',
                    'precautions': '皮肤病患者禁用，饭后一小时内不宜刮痧',
                    'suitable_crowd': '肩颈不适者、亚健康人群',
                    'season': '夏季为佳'
                },
                {
                    'title': '站桩功',
                    'category': '传统功法',
                    'content': '站桩功是通过站立不动的姿势进行锻炼的养生功法。基本姿势：两脚分开与肩同宽，膝微屈，双手抱圆于胸前。',
                    'benefits': '培元固本、增强体力、改善气血、提高专注力',
                    'precautions': '初练时间不宜过长，循序渐进',
                    'suitable_crowd': '学习压力大的学生、脑力工作者',
                    'season': '四季皆可'
                },
                {
                    'title': '茶道养生',
                    'category': '饮食养生',
                    'content': '中国茶道讲究茶的选择、泡制和品饮。绿茶清热，红茶暖胃，普洱茶降脂，乌龙茶去腻，白茶清火。',
                    'benefits': '提神醒脑、抗氧化、降血脂、助消化',
                    'precautions': '空腹不宜饮浓茶，睡前少饮',
                    'suitable_crowd': '大学生、职场人士',
                    'season': '春饮花茶、夏饮绿茶、秋饮乌龙、冬饮红茶'
                },
                {
                    'title': '经络拍打',
                    'category': '中医疗法',
                    'content': '通过拍打身体经络和穴位，疏通气血、排除毒素。常拍打手三阴三阳经、足三阴三阳经等。',
                    'benefits': '疏通经络、促进血液循环、缓解疲劳、增强免疫',
                    'precautions': '力度适中，避免过重造成损伤',
                    'suitable_crowd': '久坐人群、运动不足者',
                    'season': '全年适用'
                },
                {
                    'title': '马王堆导引术',
                    'category': '传统功法',
                    'content': '导引术是通过肢体运动、呼吸吐纳、意念活动来锻炼身体的传统养生方法。包括马王堆导引术、易筋经等。',
                    'benefits': '舒筋活络、调和气血、强身健体、延年益寿',
                    'precautions': '呼吸要自然，动作要缓慢',
                    'suitable_crowd': '各年龄段人群',
                    'season': '春夏秋冬皆宜'
                }
            ]
            
            for item in sample_knowledge:
                knowledge = Knowledge(**item)
                db.session.add(knowledge)
            
            db.session.commit()

# 路由
@app.route('/')
def index():
    # 获取所有养生知识
    knowledges = Knowledge.query.all()
    
    # 获取热门内容（按浏览量排序）
    popular = Knowledge.query.order_by(Knowledge.view_count.desc()).limit(3).all()
    
    # 如果用户登录，获取个性化推荐
    recommendations = []
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            # 基于用户搜索历史和收藏推荐
            favorited_categories = db.session.query(Knowledge.category).join(
                Favorite, Favorite.knowledge_id == Knowledge.id
            ).filter(Favorite.user_id == user.id).distinct().all()
            
            if favorited_categories:
                categories = [c[0] for c in favorited_categories]
                recommendations = Knowledge.query.filter(
                    Knowledge.category.in_(categories)
                ).order_by(db.func.random()).limit(3).all()
    
    # 如果没有个性化推荐，随机推荐
    if not recommendations:
        recommendations = Knowledge.query.order_by(db.func.random()).limit(3).all()
    
    return render_template('index.html', 
                         knowledges=knowledges, 
                         popular=popular,
                         recommendations=recommendations,
                         user_logged_in='user_id' in session,
                         username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 验证用户是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'error')
            return redirect(url_for('register'))
        
        # 创建新用户
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('index'))

# API路由
# 在 app.py 的 API 路由部分，添加这个新函数
@app.route('/api/user/profile')
@login_required
def user_profile():
    user_id = session['user_id']

    # 1. 查询统计数据
    favorite_count = Favorite.query.filter_by(user_id=user_id).count()
    comment_count = Comment.query.filter_by(user_id=user_id).count()

    # 2. 查询所有收藏的知识条目
    favorites = Favorite.query.filter_by(user_id=user_id).order_by(Favorite.created_at.desc()).all()

    # 3. 构建收藏列表
    favorites_data = []
    for fav in favorites:
        knowledge = fav.knowledge
        favorites_data.append({
            'id': knowledge.id,
            'title': knowledge.title,
            'category': knowledge.category,
            'content_preview': knowledge.content[:80] + '...' if len(knowledge.content) > 80 else knowledge.content
        })

    # 4. 返回JSON数据
    return jsonify({
        'username': session.get('username'),
        'stats': {
            'favorites': favorite_count,
            'comments': comment_count
        },
        'favorites': favorites_data
    })

@app.route('/api/search')
def search():
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({'results': []})
    
    # 记录搜索历史
    if 'user_id' in session:
        search_history = SearchHistory(
            user_id=session['user_id'],
            keyword=keyword
        )
        db.session.add(search_history)
        db.session.commit()
    
    # 搜索知识库
    results = Knowledge.query.filter(
        db.or_(
            Knowledge.title.contains(keyword),
            Knowledge.content.contains(keyword),
            Knowledge.category.contains(keyword)
        )
    ).all()
    
    return jsonify({
        'results': [{
            'id': k.id,
            'title': k.title,
            'category': k.category,
            'content': k.content[:100] + '...' if len(k.content) > 100 else k.content
        } for k in results]
    })

# ... (在 app.py 的其他路由后面, API路由前面)

# 路由: 显示体质测试页面
@app.route('/test')
def constitution_test():
    return render_template('test.html', username=session.get('username', None))

# API路由: 处理体质测试提交
# 在 app.py 中，替换这个函数

@app.route('/api/submit_test', methods=['POST'])
def submit_constitution_test():
    answers = request.json
    
    # 定义题目信息 (题目ID -> 体质, 是否反向计分)
    # 关键修复：为平和质的指定题目添加 True 标记
    questions_map = {
        # ... (其他体质不变, 都是 False)
        'q_yangxu_1': ('yangxu', False), 'q_yangxu_2': ('yangxu', False), 'q_yangxu_3': ('yangxu', False),'q_yangxu_4': ('yangxu', False), 'q_yangxu_5': ('yangxu', False), 'q_yangxu_6': ('yangxu', False),
        'q_yinxu_1': ('yinxu', False), 'q_yinxu_2': ('yinxu', False), 'q_yinxu_3': ('yinxu', False), 'q_yinxu_4': ('yinxu', False),'q_yinxu_5': ('yinxu', False), 'q_yinxu_6': ('yinxu', False), 'q_yinxu_7': ('yinxu', False),
        'q_qixu_1': ('qixu', False), 'q_qixu_2': ('qixu', False), 'q_qixu_3': ('qixu', False), 'q_qixu_4': ('qixu', False),'q_qixu_5': ('qixu', False), 'q_qixu_6': ('qixu', False), 'q_qixu_7': ('qixu', False), 'q_qixu_8': ('qixu', False),
        'q_tanshi_1': ('tanshi', False), 'q_tanshi_2': ('tanshi', False), 'q_tanshi_3': ('tanshi', False), 'q_tanshi_4': ('tanshi', False),'q_tanshi_5': ('tanshi', False), 'q_tanshi_6': ('tanshi', False), 'q_tanshi_7': ('tanshi', False), 'q_tanshi_8': ('tanshi', False),
        'q_shire_1': ('shire', False), 'q_shire_2': ('shire', False), 'q_shire_3': ('shire', False), 'q_shire_4': ('shire', False),'q_shire_5': ('shire', False), 'q_shire_6': ('shire', False), 'q_shire_7': ('shire', False),
        'q_xueyu_1': ('xueyu', False), 'q_xueyu_2': ('xueyu', False), 'q_xueyu_3': ('xueyu', False), 'q_xueyu_4': ('xueyu', False),'q_xueyu_5': ('xueyu', False), 'q_xueyu_6': ('xueyu', False), 'q_xueyu_7': ('xueyu', False),
        'q_tebing_1': ('tebing', False), 'q_tebing_2': ('tebing', False), 'q_tebing_3': ('tebing', False), 'q_tebing_4': ('tebing', False),'q_tebing_5': ('tebing', False), 'q_tebing_6': ('tebing', False), 'q_tebing_7': ('tebing', False),
        'q_qiyu_1': ('qiyu', False), 'q_qiyu_2': ('qiyu', False), 'q_qiyu_3': ('qiyu', False), 'q_qiyu_4': ('qiyu', False),'q_qiyu_5': ('qiyu', False), 'q_qiyu_6': ('qiyu', False), 'q_qiyu_7': ('qiyu', False),
        
        # 平和质题目，根据文档添加逆向计分标记
        'q_pinghe_1': ('pinghe', False), 
        'q_pinghe_2': ('pinghe', True),  # 逆向
        'q_pinghe_3': ('pinghe', True),  # 逆向
        'q_pinghe_4': ('pinghe', True),  # 逆向
        'q_pinghe_5': ('pinghe', True),  # 逆向
        'q_pinghe_6': ('pinghe', False),
        'q_pinghe_7': ('pinghe', True),  # 逆向
        'q_pinghe_8': ('pinghe', True)   # 逆向
    }

    raw_scores = {}
    item_counts = {}

    for q_id, value in answers.items():
        if q_id in questions_map:
            constitution, is_reversed = questions_map[q_id]
            
            # 初始化分数和计数器
            raw_scores.setdefault(constitution, 0)
            item_counts.setdefault(constitution, 0)

            score = int(value)
            if is_reversed:
                score = 6 - score  # 逆向计分逻辑
            
            raw_scores[constitution] += score
            item_counts[constitution] += 1

    converted_scores = {}
    for t, raw_score in raw_scores.items():
        count = item_counts.get(t, 1) # 防止除零错误
        converted_score = ((raw_score - count) / (count * 4)) * 100
        converted_scores[t] = converted_score

    results = []
    constitution_names = { 'pinghe': '平和质', 'yangxu': '阳虚质', 'yinxu': '阴虚质', 'qixu': '气虚质', 'tanshi': '痰湿质', 'shire': '湿热质', 'xueyu': '血瘀质', 'tebing': '特禀质', 'qiyu': '气郁质' }
    
    pinghe_score = converted_scores.get('pinghe', 0)
    other_scores = {k: v for k, v in converted_scores.items() if k != 'pinghe'}

    is_pinghe = False
    if pinghe_score >= 60:
        if all(s < 30 for s in other_scores.values()):
            results.append(f"是 {constitution_names['pinghe']}")
            is_pinghe = True
        elif all(s < 40 for s in other_scores.values()):
            results.append(f"基本是 {constitution_names['pinghe']}")
            is_pinghe = True

    if not is_pinghe:
        for t, score in other_scores.items():
            if score >= 40:
                results.append(f"是 {constitution_names[t]}")
            elif 30 <= score < 40:
                results.append(f"倾向是 {constitution_names[t]}")
    
    if not results:
        results.append("您的体质类型不明显，趋于平和。")

    return jsonify({'results': results})

@app.route('/api/knowledge/<int:id>')
def get_knowledge(id):
    knowledge = Knowledge.query.get_or_404(id)
    
    # 增加浏览量
    knowledge.view_count += 1
    db.session.commit()
    
    # 检查是否已收藏
    is_favorited = False
    if 'user_id' in session:
        favorite = Favorite.query.filter_by(
            user_id=session['user_id'],
            knowledge_id=id
        ).first()
        is_favorited = favorite is not None
    
    # 获取评论
    comments = Comment.query.filter_by(knowledge_id=id).order_by(Comment.created_at.desc()).all()
    
    return jsonify({
        'id': knowledge.id,
        'title': knowledge.title,
        'category': knowledge.category,
        'content': knowledge.content,
        'benefits': knowledge.benefits,
        'precautions': knowledge.precautions,
        'suitable_crowd': knowledge.suitable_crowd,
        'season': knowledge.season,
        'video_url': knowledge.video_url,
        'view_count': knowledge.view_count,
        'is_favorited': is_favorited,
        'comments': [{
            'id': c.id,
            'username': c.user.username,
            'content': c.content,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
        } for c in comments]
    })

@app.route('/api/favorite/<int:knowledge_id>', methods=['POST'])
@login_required
def toggle_favorite(knowledge_id):
    knowledge = Knowledge.query.get_or_404(knowledge_id)
    
    favorite = Favorite.query.filter_by(
        user_id=session['user_id'],
        knowledge_id=knowledge_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed', 'message': '已取消收藏'})
    else:
        favorite = Favorite(
            user_id=session['user_id'],
            knowledge_id=knowledge_id
        )
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'status': 'added', 'message': '收藏成功'})

@app.route('/api/comment/<int:knowledge_id>', methods=['POST'])
@login_required
def add_comment(knowledge_id):
    knowledge = Knowledge.query.get_or_404(knowledge_id)
    content = request.json.get('content', '').strip()
    
    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400
    
    beijing_tz = timezone(timedelta(hours=8))
    
    comment = Comment(
        user_id=session['user_id'],
        knowledge_id=knowledge_id,
        content=content,
        created_at=datetime.now(beijing_tz)
    )
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'id': comment.id,
        'username': comment.user.username,
        'content': comment.content,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
    })

@app.route('/api/user/favorites')
@login_required
def user_favorites():
    favorites = Favorite.query.filter_by(user_id=session['user_id']).all()
    
    return jsonify({
        'favorites': [{
            'id': f.knowledge.id,
            'title': f.knowledge.title,
            'category': f.knowledge.category,
            'created_at': f.created_at.strftime('%Y-%m-%d')
        } for f in favorites]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)