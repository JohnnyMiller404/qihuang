// static/script.js (完整数据版)

// 全局变量
let currentCategory = 'all';
let myChart = null;

document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    initializeGraph();
    autoHideFlashMessages();
    initializeAnimations();
});

function setupEventListeners() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') performSearch();
        });
    }

    window.addEventListener('click', function(e) {
        const modal = document.getElementById('knowledgeModal');
        const searchModal = document.getElementById('searchModal');
        const personalCenterModal = document.getElementById('personalCenterModal');
        if (e.target === modal) closeModal();
        if (e.target === searchModal) closeSearchModal();
        if (e.target === personalCenterModal) closePersonalCenterModal();
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    const personalCenterBtn = document.getElementById('personalCenterBtn');
    if (personalCenterBtn) {
        personalCenterBtn.addEventListener('click', showPersonalCenter);
    }
}

// --- ECharts 放射状知识图谱逻辑 ---

function initializeGraph() {
    const chartDom = document.getElementById('graphChart');
    if (!chartDom) return;

    if (myChart != null && myChart != "" && myChart != undefined) {
        myChart.dispose();
    }
    myChart = echarts.init(chartDom);

    // 1. 数据准备 (已替换为文档中的完整详细内容)
    const data = {
        name: "大学生养生\n核心痛点",
        children: [
            {
                name: "筋骨肢体",
                children: [
                    {
                        name: "肩颈酸痛",
                        info: {
                            solutions: [
                                "中医推拿（滚法松筋：以小鱼际为着力点，沿肩颈肌群做滚动按压；肩井穴按揉：以拇指指腹按揉肩井穴，力度以酸胀为宜）",
                                "五禽戏·虎举/鹿抵动作：虎举需双手向上举至头顶再下落；鹿抵需腰部扭转，头部随身体转动",
                                "苗族草药热敷（肩颈专用药包：含透骨草、伸筋草等药材，加热后敷于肩颈）"
                            ],
                            scenarios: [
                                "久坐看电脑/手机40分钟后",
                                "教室课间10分钟休息",
                                "宿舍睡前15分钟放松",
                                "图书馆自习1小时后的间隙"
                            ],
                            taboos: [
                                "急性扭伤未消肿（48小时内）忌大力推拿",
                                "肩颈皮肤破损、湿疹处禁用热敷",
                                "颈椎不稳（如颈椎间盘突出急性期）者避免过度扭转头部",
                                "餐后1小时内不做大幅度肩颈动作"
                            ],
                            effects: [
                                "即时缓解肌肉紧张（约80%使用者反馈肩颈僵硬减轻）",
                                "2周改善肩颈僵硬（可正常完成头部左右转动各45°）",
                                "4周提升肩颈活动度10%（前屈、后伸角度增加）",
                                "长期坚持（≥8周）改善圆肩、驼背体态"
                            ]
                        }
                    },
                    {
                        name: "腰椎疼痛",
                        info: {
                            solutions: [
                                "中医正骨推拿（摸骨正脊术：通过触诊定位腰椎错位节段，轻柔调整关节位置）",
                                "八段锦·两手攀足固肾腰：双腿伸直，双手沿腿前侧下伸至脚踝，缓慢起身",
                                "中药熏洗（腰部专用配方：含艾叶、红花等，煮水后熏蒸腰部）"
                            ],
                            scenarios: [
                                "久坐学习（≥1小时）后",
                                "腰痛初期（隐痛、酸胀）居家放松",
                                "宿舍午休后5分钟舒缓",
                                "运动（如跑步、健身）后腰部不适时"
                            ],
                            taboos: [
                                "腰椎骨折、脱位急性期（2周内）禁用任何推拿/动作",
                                "孕妇慎用推拿、熏洗（避免刺激腰部）",
                                "腰椎间盘突出急性期忌弯腰、扭转动作",
                                "熏洗温度忌超过50℃（避免烫伤皮肤）"
                            ],
                            effects: [
                                "1周减轻腰部酸痛（久坐后疼痛持续时间缩短）",
                                "3周改善腰椎活动度（可完成弯腰手触地动作）",
                                "6周缓解久坐后腰部坠胀（坐下1小时内无明显不适）",
                                "长期坚持（≥12周）降低腰痛复发频率（由每周2-3次降至每月1次内）"
                            ]
                        }
                    },
                    {
                        name: "手腕腱鞘炎",
                        info: {
                            solutions: [
                                "针灸（阿是穴：痛点局部针刺；合谷穴、阳溪穴：辅助针刺，留针15分钟）",
                                "苗医药熏浴液（手腕浸泡：含土茯苓、桂枝等药材，水温38-40℃，浸泡15分钟）",
                                "中医推拿（腕部理筋手法：以拇指沿腕部肌腱走向做按揉、拨筋）"
                            ],
                            scenarios: [
                                "长期打字（≥2小时）/写作业后",
                                "宿舍休息时段（睡前、晨起）",
                                "图书馆自习1小时后的间隙",
                                "居家网课（连续用鼠标/键盘）后"
                            ],
                            taboos: [
                                "手腕皮肤破溃、溃疡处禁用针灸、熏浴",
                                "急性炎症期（红肿热痛明显）忌用力推拿",
                                "熏浴时长不超过20分钟（避免皮肤浸渍）",
                                "针灸需由执业中医师操作（禁止自行针刺）"
                            ],
                            effects: [
                                "3天减轻炎症疼痛（按压痛缓解）",
                                "2周缓解手腕活动受限（可正常完成握拳、伸展动作）",
                                "4周改善手腕发力不适感（打字、握笔时无明显疼痛）",
                                "长期坚持（≥6周）降低腱鞘炎复发率（由每月1-2次降至每季度1次内）"
                            ]
                        }
                    },
                    {
                        name: "关节疼痛",
                        info: {
                            solutions: [
                                "苗医药熏浴液（关节浸泡：含独活、牛膝等药材，水温38-40℃，浸泡20分钟）",
                                "中医推拿（关节周围理筋：以拇指按揉膝关节周围的血海、梁丘穴，踝关节的昆仑、太溪穴）",
                                "八段锦·调理脾胃须单举（关节联动：单臂上举、下落，带动膝/踝关节轻微活动）"
                            ],
                            scenarios: [
                                "运动（如跑步、跳绳）后关节不适",
                                "慢性关节疼痛（如受凉后隐痛）时",
                                "宿舍休息时段（睡前、晨起）",
                                "居家网课（久坐后关节僵硬）放松"
                            ],
                            taboos: [
                                "关节急性损伤（如扭伤）肿胀期（48小时内）禁用熏浴",
                                "关节皮肤破溃、皮疹处禁用任何操作",
                                "关节畸形（如O型腿、踝关节错位）者忌过度活动",
                                "熏浴时长不超过20分钟（避免皮肤浸渍）"
                            ],
                            effects: [
                                "3天减轻关节疼痛（按压痛、活动痛缓解）",
                                "2周改善关节活动度（膝关节屈伸角度增加，踝关节可正常内翻/外翻）",
                                "4周缓解运动后不适（运动后关节疼痛持续时间缩短）",
                                "长期坚持（≥8周）降低关节疼痛频率（由每周2-3次降至每月1次内）"
                            ]
                        }
                    }
                ]
            },
            {
                name: "精神情志",
                children: [
                    {
                        name: "失眠",
                        info: {
                            solutions: [
                                "艾灸（神门、涌泉穴灸疗：神门穴（腕部）、涌泉穴（足底）各灸5分钟）",
                                "太极拳（睡前舒缓动作：云手、揽雀尾，动作缓慢，配合深呼吸）",
                                "中医情志疗法（以静安神法：睡前静坐5分钟，专注呼吸，排除杂念）"
                            ],
                            scenarios: [
                                "睡前1-2小时",
                                "宿舍夜间（22:00-23:00）放松",
                                "居家网课睡前",
                                "压力大（如考试前）失眠时"
                            ],
                            taboos: [
                                "空腹、过饱时不艾灸（避免胃肠不适）",
                                "艾灸时远离床单、书籍等易燃物（防止火灾）",
                                "严重失眠（连续≥3天入睡困难）需配合专业心理/药物治疗",
                                "太极拳动作忌过度用力、追求速度（以舒缓为宜）"
                            ],
                            effects: [
                                "1周缩短入睡时间（从30分钟以上缩短至15分钟内）",
                                "3周改善睡眠质量（夜间醒来次数从2-3次减少至0-1次）",
                                "6周减少夜间醒来次数（可连续睡眠6-7小时）",
                                "长期坚持（≥12周）稳定睡眠节律（固定时间入睡、起床）"
                            ]
                        }
                    },
                    {
                        name: "焦虑情绪",
                        info: {
                            solutions: [
                                "太极拳（全身舒缓动作：整套简化24式，动作缓慢，配合腹式呼吸）",
                                "八段锦（调节呼吸节奏：每式配合3-5次深呼吸，专注动作与气息）",
                                "中医情志疗法（以情胜情法：焦虑时听舒缓音乐、做轻度拉伸，转移注意力）"
                            ],
                            scenarios: [
                                "压力大（如作业截止、考试前）时",
                                "情绪低落（如社交受挫）时",
                                "宿舍休息时段（午后、傍晚）",
                                "图书馆自习间隙（学习1小时后）"
                            ],
                            taboos: [
                                "严重精神疾病（如抑郁症、焦虑症）需在专业医师指导下进行",
                                "情绪激动（如愤怒、哭泣）时忌剧烈动作（避免心率过快）",
                                "太极拳动作忌过度追求难度、标准度（以舒适为宜）",
                                "情志疗法需结合自身状态（避免强迫自己“放松”）"
                            ],
                            effects: [
                                "即时缓解情绪紧张（心率从100次/分钟以上降至80次/分钟内）",
                                "2周改善焦虑状态（对压力事件的恐惧心理减轻）",
                                "4周提升情绪调节能力（可自主通过动作/呼吸平复情绪）",
                                "长期坚持（≥8周）稳定心理状态（情绪波动频率降低）"
                            ]
                        }
                    },
                    {
                        name: "疲劳乏力",
                        info: {
                            solutions: [
                                "五禽戏（增强气血运行：整套动作，重点做熊晃、鸟飞式，配合深呼吸）",
                                "中药茶饮（黄芪党参配方：取黄芪5g、党参3g，开水冲泡代茶饮，每日1剂）",
                                "中医艾灸（足三里穴灸疗：用艾灸条灸足三里穴，每次10分钟，温度以温热为宜）"
                            ],
                            scenarios: [
                                "日常疲劳（如晨起、午后）时",
                                "精力不足（如学习时犯困）时",
                                "宿舍休息时段（午后、傍晚）",
                                "图书馆自习间隙（学习1小时后）"
                            ],
                            taboos: [
                                "外感发热（如感冒发烧）时不饮温补茶饮（避免加重发热）",
                                "空腹、过饱时不艾灸（避免胃肠不适）",
                                "五禽戏动作忌过度劳累（以轻微出汗为宜）",
                                "艾灸时远离易燃物（防止火灾）"
                            ],
                            effects: [
                                "即时提升精力（犯困时做动作后可清醒30分钟以上）",
                                "2周减轻日常疲劳（午后犯困频率降低）",
                                "4周增强身体耐受力（连续学习时间从2小时延长至3小时）",
                                "长期坚持（≥8周）改善精神状态（晨起精神饱满，无倦怠感）"
                            ]
                        }
                    }
                ]
            },
            {
                name: "脏腑感官",
                children: [
                    {
                        name: "眼睛疲劳",
                        info: {
                            solutions: [
                                "中医眼保健操（经络按压：按揉攒竹、鱼腰、四白等穴，每穴20秒）",
                                "中药熏蒸（菊花+枸杞配方：取菊花5g、枸杞10g煮水，熏蒸眼部，距离20cm）",
                                "八段锦·攒拳怒目增气力：双手握拳，双眼随拳头转动用力睁大，重复6次"
                            ],
                            scenarios: [
                                "长时间用眼（≥1小时）后",
                                "宿舍追剧/刷手机（≥30分钟）间隙",
                                "教室课后5分钟放松",
                                "图书馆阅读（纸质书/电子书）休息时"
                            ],
                            taboos: [
                                "眼部感染（如结膜炎）急性期禁用熏蒸",
                                "眼保健操忌直接按压眼球（仅按揉穴位周围）",
                                "高血压者做攒拳怒目时忌过度屏气（保持自然呼吸）",
                                "熏蒸温度不超过40℃（避免灼伤眼周皮肤）"
                            ],
                            effects: [
                                "1周缓解眼干涩、酸胀（用眼后不适感减轻）",
                                "3周改善视物模糊（看远处文字清晰度提升）",
                                "6周提升眼部耐受时长20%（连续用眼时间从40分钟延长至50分钟）",
                                "长期坚持（≥12周）降低近视加深风险（近视度数增长速度放缓）"
                            ]
                        }
                    },
                    {
                        name: "消化不良",
                        info: {
                            solutions: [
                                "中药食疗（山楂蜂蜜健胃丸：取山楂50g煮烂，加蜂蜜20g制丸，每次1丸）",
                                "腹部推拿（顺时针摩腹：以掌心绕脐周顺时针按揉，力度适中，每次5分钟）",
                                "中医艾灸（中脘穴灸疗：用艾灸盒灸中脘穴，每次10分钟，温度以温热为宜）"
                            ],
                            scenarios: [
                                "餐后腹胀（尤其是吃撑后）时",
                                "食欲不振（连续2餐进食量减少）时",
                                "宿舍休息时段（餐后1小时）",
                                "居家网课餐后30分钟放松"
                            ],
                            taboos: [
                                "急性胃肠炎（伴呕吐、腹泻）慎用腹部推拿",
                                "胃酸过多者（常有反酸）少用山楂（避免刺激胃酸分泌）",
                                "空腹、过饱时不艾灸（避免胃肠不适）",
                                "腹部皮肤破损、过敏者禁用艾灸"
                            ],
                            effects: [
                                "即时缓解餐后腹胀（按揉后10分钟内排气、胀痛减轻）",
                                "2周改善食欲不振（进食量恢复至正常水平）",
                                "4周提升消化效率（餐后饱胀感持续时间从2小时缩短至30分钟）",
                                "长期坚持（≥8周）调理脾胃功能（大便规律、消化能力增强）"
                            ]
                        }
                    },
                    {
                        name: "痛经",
                        info: {
                            solutions: [
                                "中药热敷（暖宫药包：含益母草、当归等药材，加热后敷于下腹部）",
                                "铺灸（督脉灸：经期前1周，沿脊柱督脉铺姜泥+艾绒施灸，每次20分钟）",
                                "中医推拿（腹部揉按：以掌心绕脐周顺时针轻揉，每次10分钟）"
                            ],
                            scenarios: [
                                "经期前后（腹痛发作时）",
                                "宿舍休息时段",
                                "居家网课经期放松",
                                "痛经初期（隐痛）舒缓"
                            ],
                            taboos: [
                                "孕妇禁用任何热敷、推拿、铺灸操作",
                                "月经量过多者（每日卫生巾使用≥5片）经期慎用铺灸",
                                "下腹部皮肤破损、过敏者禁用热敷",
                                "急性痛经（疼痛难忍、伴冷汗）需及时就医（排除器质性病变）"
                            ],
                            effects: [
                                "即时减轻腹痛（热敷后15分钟内疼痛缓解）",
                                "2周缓解经期坠胀（腹部下坠感减轻）",
                                "4周改善经期不适持续时间（疼痛从1-2天缩短至半天内）",
                                "长期坚持（≥3个经期）减轻痛经程度（从剧痛转为隐痛）"
                            ]
                        }
                    }
                ]
            }
        ]
    };

    // 2. 配置 ECharts 选项
    const option = {
        tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove',
            formatter: '{b}'
        },
        series: [
            {
                type: 'tree',
                data: [data],
                layout: 'radial',
                top: '10%',
                bottom: '10%',
                symbol: 'circle',
                symbolSize: 20,
                initialTreeDepth: 2,
                animationDurationUpdate: 750,
                
                // 文字强制水平
                label: {
                    position: 'top',
                    rotate: 0,
                    verticalAlign: 'middle',
                    align: 'center',
                    fontSize: 15,
                    fontWeight: 'bold',
                    color: '#8B4513',
                    distance: 8,
                    textBorderColor: '#fffaf0',
                    textBorderWidth: 3
                },

                itemStyle: {
                    color: '#8B4513',
                    borderColor: '#D2691E',
                    borderWidth: 2
                },

                leaves: {
                    label: {
                        position: 'top',
                        rotate: 0,
                        verticalAlign: 'middle',
                        align: 'center',
                        fontSize: 14,
                        color: '#5D4037',
                        fontWeight: 'normal',
                        distance: 10,
                        textBorderColor: '#fffaf0',
                        textBorderWidth: 3
                    },
                    itemStyle: {
                        color: '#FFD700',
                        borderColor: '#DAA520'
                    }
                },
                
                levels: [
                    {
                        itemStyle: {
                            color: '#8B4513',
                            borderWidth: 4,
                            borderColor: '#FFFFFF',
                            shadowBlur: 10,
                            shadowColor: 'rgba(0, 0, 0, 0.3)'
                        },
                        symbolSize: 45,
                        label: { fontSize: 20, color: '#FFFFFF', position: 'inside', rotate: 0, textBorderWidth: 0 }
                    },
                    {
                        itemStyle: { color: '#D2691E' },
                        symbolSize: 25
                    },
                    {
                        itemStyle: { color: '#FFD700' },
                        symbolSize: 15
                    }
                ]
            }
        ]
    };

    myChart.setOption(option);

    myChart.on('click', function (params) {
        if (params.data.info) {
            showDetailModal(params.data.name, params.data.info);
        }
    });

    window.addEventListener('resize', function() {
        myChart.resize();
    });
}

function showDetailModal(title, info) {
    const modal = document.getElementById('graphDetailModal');
    const titleEl = document.getElementById('detailTitle');
    const contentEl = document.getElementById('detailContent');

    titleEl.textContent = title + " - 调理方案";

    let html = '';
    html += `<div class="detail-section"><h4>🔮 非遗解决方案</h4><ul>${info.solutions.map(s => `<li>${s}</li>`).join('')}</ul></div>`;
    html += `<div class="detail-section"><h4>📍 适配场景</h4><ul>${info.scenarios.map(s => `<li>${s}</li>`).join('')}</ul></div>`;
    html += `<div class="detail-section"><h4 style="color: #d9534f;">⚠️ 操作禁忌</h4><ul>${info.taboos.map(t => `<li>${t}</li>`).join('')}</ul></div>`;
    html += `<div class="detail-section"><h4>📈 预期效果</h4><ul>${info.effects.map(e => `<li>${e}</li>`).join('')}</ul></div>`;

    contentEl.innerHTML = html;
    modal.classList.add('active');
}

function closeGraphModal() {
    const modal = document.getElementById('graphDetailModal');
    if (modal) modal.classList.remove('active');
}

async function performSearch() {
    const keyword = document.getElementById('searchInput').value.trim();
    if (!keyword) {
        showNotification('请输入搜索关键词', 'warning');
        return;
    }
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        if (data.results.length === 0) {
            showNotification('没有找到相关内容', 'info');
            return;
        }
        displaySearchResults(data.results);
    } catch (error) {
        console.error('搜索失败:', error);
        showNotification('搜索失败,请稍后重试', 'error');
    }
}

function displaySearchResults(results) {
    const searchModal = document.getElementById('searchModal');
    const searchResults = document.getElementById('searchResults');
    let html = '<div class="search-results-grid">';
    results.forEach(item => {
        html += `
            <div class="search-result-item" onclick="showKnowledgeDetail(${item.id}); closeSearchModal();">
                <div class="result-header">
                    <span class="category-badge">${item.category}</span>
                    <h4>${item.title}</h4>
                </div>
                <p>${item.content}</p>
            </div>
        `;
    });
    html += '</div>';
    searchResults.innerHTML = html;
    searchModal.style.display = 'block';
}

async function showKnowledgeDetail(id) {
    try {
        const response = await fetch(`/api/knowledge/${id}`);
        const data = await response.json();
        const modal = document.getElementById('knowledgeModal');
        const modalBody = document.getElementById('modalBody');
        
        let commentsHtml = '';
        if (data.comments && data.comments.length > 0) {
            commentsHtml = '<div class="comments-section"><h4>用户评论</h4>';
            data.comments.forEach(comment => {
                commentsHtml += `<div class="comment-item"><div class="comment-header"><strong>${comment.username}</strong><span class="comment-time">${comment.created_at}</span></div><p>${comment.content}</p></div>`;
            });
            commentsHtml += '</div>';
        }
        
        modalBody.innerHTML = `
            <div class="knowledge-detail">
                <div class="detail-header">
                    <h2>${data.title}</h2>
                    <div class="detail-tags"><span class="tag">${data.category}</span><span class="tag">${data.season}</span><span class="view-tag">👁 ${data.view_count} 次浏览</span></div>
                </div>
                <div class="detail-content">
                    <section><h3>📖 详细介绍</h3><p>${data.content}</p></section>
                    <section><h3>✨ 功效益处</h3><p>${data.benefits}</p></section>
                    <section><h3>⚠️ 注意事项</h3><p>${data.precautions}</p></section>
                    <section><h3>👥 适宜人群</h3><p>${data.suitable_crowd}</p></section>
                </div>
                <div class="detail-actions">
                    <button class="btn-favorite ${data.is_favorited ? 'favorited' : ''}" onclick="toggleFavorite(${data.id})">${data.is_favorited ? '❤️ 已收藏' : '🤍 收藏'}</button>
                    <button class="btn-comment" onclick="showCommentForm(${data.id})">💬 发表评论</button>
                </div>
                <div id="commentForm-${data.id}" class="comment-form" style="display: none;">
                    <textarea id="commentText-${data.id}" placeholder="分享您的养生心得..."></textarea>
                    <button onclick="submitComment(${data.id})">发表</button>
                </div>
                ${commentsHtml}
            </div>`;
        modal.style.display = 'block';
    } catch (error) {
        showNotification('获取详情失败', 'error');
    }
}

function closeModal() { document.getElementById('knowledgeModal').style.display = 'none'; }
function closeSearchModal() { document.getElementById('searchModal').style.display = 'none'; }

async function showPersonalCenter() {
    const modal = document.getElementById('personalCenterModal');
    const modalBody = document.getElementById('personalCenterBody');
    modal.style.display = 'block';
    modalBody.innerHTML = '<div class="loader"></div>';
    try {
        const response = await fetch('/api/user/profile');
        if (response.status === 401) {
            modal.style.display = 'none';
            showNotification('请先登录', 'warning');
            setTimeout(() => window.location.href = '/login', 1500);
            return;
        }
        const data = await response.json();
        let favoritesHtml = '<div class="favorites-grid">';
        if (data.favorites.length > 0) {
            data.favorites.forEach(item => {
                favoritesHtml += `<div class="favorite-card" onclick="showKnowledgeDetail(${item.id}); closePersonalCenterModal();"><span class="category-badge">${item.category}</span><h4>${item.title}</h4><p>${item.content_preview}</p></div>`;
            });
        } else {
            favoritesHtml += '<p>您还没有任何收藏哦。</p>';
        }
        favoritesHtml += '</div>';
        modalBody.innerHTML = `<div class="personal-center-content"><h3>${data.username}的个人中心</h3><div class="user-stats"><div class="stat-box"><span class="stat-number">${data.stats.favorites}</span><span class="stat-label">我的收藏</span></div><div class="stat-box"><span class="stat-number">${data.stats.comments}</span><span class="stat-label">我的评论</span></div></div><h4>我收藏的内容</h4>${favoritesHtml}</div>`;
    } catch (error) {
        modalBody.innerHTML = '<p>加载失败。</p>';
    }
}
function closePersonalCenterModal() { document.getElementById('personalCenterModal').style.display = 'none'; }

function showNotification(message, type = 'info') {
    const n = document.createElement('div'); n.className = `flash-message flash-${type}`; n.textContent = message; document.body.appendChild(n);
    setTimeout(() => { n.style.opacity = '1'; n.style.transform = 'translateX(0)'; }, 10);
    setTimeout(() => { n.style.opacity = '0'; n.style.transform = 'translateX(100%)'; setTimeout(() => n.remove(), 300); }, 3000);
}
function autoHideFlashMessages() { document.querySelectorAll('.flash-message').forEach(msg => { setTimeout(() => { msg.style.opacity = '0'; msg.style.transform = 'translateX(100%)'; setTimeout(() => msg.remove(), 300); }, 3000); }); }
function initializeAnimations() { const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('animate-in'); }); }, { threshold: 0.1 }); document.querySelectorAll('.knowledge-item, .popular-card, .knowledge-card').forEach(el => observer.observe(el)); }
function showCommentForm(id) { const form = document.getElementById(`commentForm-${id}`); if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none'; }
async function toggleFavorite(id) {
    try { const res = await fetch(`/api/favorite/${id}`, { method: 'POST', headers: { 'Content-Type': 'application/json' } }); 
    if (res.status === 401) { showNotification('请先登录', 'warning'); setTimeout(() => window.location.href = '/login', 1500); return; }
    const d = await res.json(); showNotification(d.message, 'success'); 
    const btn = document.querySelector('.btn-favorite'); if (btn) { btn.classList.toggle('favorited', d.status === 'added'); btn.innerHTML = d.status === 'added' ? '❤️ 已收藏' : '🤍 收藏'; } } catch (e) { showNotification('操作失败', 'error'); }
}
async function submitComment(id) {
    const t = document.getElementById(`commentText-${id}`); const c = t.value.trim(); if (!c) { showNotification('请输入评论', 'warning'); return; }
    try { const res = await fetch(`/api/comment/${id}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content: c }) });
    if (res.status === 401) { showNotification('请先登录', 'warning'); return; } showNotification('评论成功', 'success'); t.value = ''; showKnowledgeDetail(id); } catch (e) { showNotification('评论失败', 'error'); }
}
function filterByCategory(cat) {
    currentCategory = cat; document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active')); event.target.classList.add('active');
    document.querySelectorAll('.knowledge-item').forEach(item => { if (cat === 'all' || item.dataset.category === cat) { item.style.display = 'block'; item.classList.add('fade-in'); } else { item.style.display = 'none'; } });
}