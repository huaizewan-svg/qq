<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>职场嘴替 - 深度吐槽助手</title>
    
    <!-- 1. Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              'paper': '#fafafa',
              'ink': '#18181b',
              'stamp': '#dc2626',
              'subtle': '#71717a',
            },
            fontFamily: {
              serif: ['"Noto Serif SC"', 'serif'],
              sans: ['"Inter"', 'sans-serif'],
              mono: ['"Courier New"', 'monospace'],
            },
            animation: {
              'bounce-slow': 'bounce 3s infinite',
              'fade-in-up': 'fadeInUp 0.5s ease-out forwards',
              'progress-stripe': 'progressStripe 1s linear infinite',
            },
            keyframes: {
              fadeInUp: {
                '0%': { opacity: '0', transform: 'translateY(10px)' },
                '100%': { opacity: '1', transform: 'translateY(0)' },
              },
              progressStripe: {
                '0%': { backgroundPosition: '40px 0' },
                '100%': { backgroundPosition: '0 0' },
              }
            }
          }
        }
      }
    </script>

    <!-- 2. Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    
    <!-- 3. Custom Styles -->
    <style>
      body {
        background-color: #fafafa;
        color: #18181b;
      }
      ::-webkit-scrollbar {
        width: 8px;
      }
      ::-webkit-scrollbar-track {
        background: #f4f4f5; 
      }
      ::-webkit-scrollbar-thumb {
        background: #d4d4d8; 
        border-radius: 4px;
      }
      ::-webkit-scrollbar-thumb:hover {
        background: #a1a1aa; 
      }
      .custom-paper-texture {
        background-image: radial-gradient(#d4d4d8 1px, transparent 1px);
        background-size: 20px 20px;
      }
    </style>

    <!-- 4. Babel for JSX compilation in browser -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- 5. Import Map for Modules -->
    <script type="importmap">
    {
      "imports": {
        "react": "https://esm.sh/react@18.2.0",
        "react-dom/client": "https://esm.sh/react-dom@18.2.0/client",
        "lucide-react": "https://esm.sh/lucide-react@0.292.0",
        "@google/genai": "https://esm.sh/@google/genai@0.1.1",
        "html2canvas": "https://esm.sh/html2canvas@1.4.1",
        "jspdf": "https://esm.sh/jspdf@2.5.1"
      }
    }
    </script>
</head>
<body>
    <div id="root"></div>

    <!-- MAIN APP LOGIC -->
    <script type="text/babel" data-type="module">
        import React, { useState, useEffect, useRef } from 'react';
        import ReactDOM from 'react-dom/client';
        import { GoogleGenAI } from '@google/genai';
        import html2canvas from 'html2canvas';
        import { jsPDF } from 'jspdf';
        import { 
          Send, Trash2, Copy, RefreshCw, MessageSquareQuote, AlertTriangle, 
          Flame, History, X, BookOpen, Coffee, PenTool, Scroll, Gavel, 
          Zap, Feather, Edit3, Check, ZoomIn, ZoomOut, Type, Bold, 
          Italic, Underline, FileDown, Share2 
        } from 'lucide-react';

        // ==========================================
        // CONFIGURATION
        // ==========================================
        
        // ⚠️⚠️⚠️ 请在这里填入你的 API KEY ⚠️⚠️⚠️
        const API_KEY = '在此处填写你的_GEMINI_API_KEY'; 

        // ==========================================
        // DATA & CONSTANTS
        // ==========================================

        const LOADING_TEXTS = [
          "火力装填中...", "正在翻阅《厚黑学》...", "研读《演员的自我修养》...",
          "分析画饼化学成分...", "计算黑锅几何直径...", "查询《糊弄学导论》...",
          "联系精神科床位...", "测算今日摸鱼指数...", "加载阴阳怪气语音包...",
          "酝酿优美中国话...", "试图理解领导脑回路...", "翻译“收到”的真实含义...",
          "检索《高情商回复指南》..."
        ];

        const PROMPTS = {
          ACADEMIC: `
            你是一位专门研究"国企行政低效与领导行为异常"的社会学教授。请将用户提供的素材视为一个"典型临床案例"，写一篇微型学术论文/调研报告。
            **风格要求**：
            1. **一本正经胡说八道**：大量使用学术名词（如"权力寻租"、"帕金森定律"、"达克效应"、"认知失调"），将领导的愚蠢行为上升到理论高度。
            2. **格式严谨**：包含【摘要】、【案例分析】、【核心悖论】、【结论与建议】。
            3. **语气冷漠客观**：像在解剖一只青蛙一样解剖你的领导，用最冷静的语言描述最荒谬的事实。
            4. **引用文献**：可以编造一些看起来很专业的参考文献（例如：《论草台班子的自我修养》2024版）。
          `,
          LITERARY: `
            你是一位当代鲁迅，一位犀利的职场讽刺作家。请根据素材写一篇杂文。
            **风格要求**：
            1. **笔锋犀利**：像手术刀一样剖析人性，使用"吃人"、"看客"、"铁屋子"等意象的现代变体。
            2. **比喻精妙**：将领导比作某种具体的、令人不适的事物。
            3. **深刻**：透过现象看本质，批判不仅限于个人，更指向这种腐朽的职场生态。
            4. **冷幽默**：让人看着看着就笑了，笑着笑着就想哭。
          `,
          POETRY: `
            你是一位怀才不遇、在国企受尽折磨的疯癫诗人（可以参考李白醉酒后的狂放，或者现代派诗人的虚无）。
            **风格要求**：
            1. **体裁不限**：可以是七言律诗（打油诗方向），也可以是现代讽刺长诗，或者宋词（如《声声慢·上班如上坟》）。
            2. **辞藻**：可以使用古语，但要通过古今对比产生荒谬感（例如："唯见长江天际流，PPT里写春秋"）。
            3. **情绪**：极度的悲愤化作极度的狂放，嘲笑权力的虚无。
          `,
          RAGE: `
            你是一位百度贴吧/虎扑/微博的"暴躁老哥"，著名的互联网"祖安状元"。
            **风格要求**：
            1. **极度口语化**：怎么爽怎么骂（注意不含脏字，但攻击性极强）。
            2. **阴阳怪气**：熟练使用反语、嘲讽技能（"不会吧不会吧"、"大聪明的操作"）。
            3. **情绪宣泄**：多用感叹号，语速极快，逻辑直接粗暴，不讲大道理，只讲大实话。
            4. **梗**：大量使用互联网热梗。
          `
        };

        const STYLES = [
          { id: 'ACADEMIC', name: '牛马学术期刊', icon: <Gavel className="w-4 h-4" />, desc: '一本正经地胡说八道，引用《自然·摸鱼》' },
          { id: 'LITERARY', name: '鲁迅代笔版', icon: <PenTool className="w-4 h-4" />, desc: '犀利毒舌，直面惨淡的职场人生' },
          { id: 'POETRY', name: '发疯吟湿版', icon: <Scroll className="w-4 h-4" />, desc: '七步成诗，字字泣血，句句带刺' },
          { id: 'RAGE', name: '祖安状元版', icon: <Zap className="w-4 h-4" />, desc: '纯粹的情绪输出，高强度的互联网嘴臭' },
        ];

        const THEMES = {
          ACADEMIC: {
            container: "bg-white border border-slate-300 shadow-sm",
            header: "bg-slate-50 border-b border-slate-300",
            headerLabel: "text-slate-600 font-serif font-bold tracking-tight",
            body: "font-serif text-slate-800 leading-relaxed",
            editor: "bg-transparent font-serif text-slate-800 placeholder-slate-300",
            h1: "text-2xl font-bold text-center text-slate-900 mb-6 pb-4 border-b border-slate-200",
            h2: "text-lg font-bold text-slate-800 mt-6 mb-2 border-l-4 border-blue-800 pl-3",
            p: "text-justify indent-8 mb-4",
            highlight: "bg-blue-50 text-blue-900 px-1 mx-0.5 rounded font-medium",
            list: "list-decimal ml-6 text-slate-700",
            footer: "text-slate-400 font-serif text-xs border-t border-slate-100 pt-4 mt-8 text-center"
          },
          LITERARY: {
            container: "bg-[#fffdf5] border-4 border-black shadow-[12px_12px_0px_0px_rgba(24,24,27,0.2)]",
            header: "bg-[#fffdf5] border-b-2 border-black",
            headerLabel: "text-black font-serif font-black tracking-widest",
            body: "font-serif text-[#2c2c2c] leading-loose",
            editor: "bg-transparent font-serif text-[#2c2c2c] placeholder-gray-300",
            h1: "text-3xl font-black text-black mb-8 pb-4 border-b-4 border-[#dc2626]",
            h2: "text-xl font-bold text-[#dc2626] mt-8 mb-4 flex items-center gap-2 before:content-['§'] before:text-gray-400",
            p: "text-justify mb-6 tracking-wide",
            highlight: "text-[#dc2626] font-bold mx-1",
            list: "list-disc ml-6 text-gray-700 marker:text-[#dc2626]",
            footer: "text-gray-400 font-serif italic text-sm mt-12 pt-4 border-t border-gray-200 text-center"
          },
          POETRY: {
            container: "bg-[#f4f4f4] border-none shadow-[inset_0_0_20px_rgba(0,0,0,0.05)]",
            header: "bg-transparent border-b border-gray-300",
            headerLabel: "text-gray-500 font-serif italic",
            body: "font-serif text-gray-700 leading-[2.5] text-center",
            editor: "bg-transparent font-serif text-gray-700 text-center placeholder-gray-300",
            h1: "text-4xl font-light text-gray-900 mb-10 mt-4 italic tracking-widest",
            h2: "text-xl font-medium text-teal-800 mt-8 mb-4",
            p: "mb-6 whitespace-pre-wrap",
            highlight: "text-teal-900 font-medium border-b border-teal-800/30",
            list: "list-none space-y-2 text-gray-600",
            footer: "text-gray-300 font-serif text-xs mt-16 text-center tracking-[0.5em]"
          },
          RAGE: {
            container: "bg-stone-200 border-4 border-stone-800 shadow-[8px_8px_0px_0px_#1c1917]",
            header: "bg-stone-800 text-stone-200 border-b-4 border-stone-800",
            headerLabel: "font-sans font-black uppercase tracking-tighter text-stone-200",
            body: "font-sans font-bold text-stone-900 leading-tight",
            editor: "bg-transparent font-sans font-bold text-stone-900 placeholder-stone-500",
            h1: "text-4xl md:text-5xl font-black uppercase mb-8 transform -rotate-1 inline-block bg-stone-900 text-stone-100 px-4 py-2 border-4 border-transparent shadow-[4px_4px_0px_0px_rgba(0,0,0,0.2)]",
            h2: "text-2xl font-black bg-stone-100 text-stone-900 border-2 border-stone-900 inline-block px-2 py-1 transform rotate-1 mt-8 mb-4 shadow-[2px_2px_0px_0px_rgba(0,0,0,0.2)]",
            p: "mb-4",
            highlight: "bg-stone-900 text-stone-100 px-2 mx-1 transform -skew-x-6 inline-block",
            list: "list-none font-black text-xl space-y-1 ml-0 uppercase text-stone-800",
            footer: "text-stone-500 font-black text-xs mt-8 border-t-4 border-stone-800 pt-4 uppercase tracking-widest"
          }
        };

        const FONT_SIZES = ['text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl'];
        const FONT_FAMILIES = [
            { label: '默认', value: 'default' },
            { label: '衬线 (Serif)', value: 'font-serif' },
            { label: '无衬线 (Sans)', value: 'font-sans' },
            { label: '等宽 (Mono)', value: 'font-mono' },
        ];

        // ==========================================
        // SERVICES
        // ==========================================

        const generateRoastStream = async (context, style, onChunk) => {
          if (!API_KEY || API_KEY.includes('在此处填写')) {
            alert("请在代码中填写有效的 API Key");
            throw new Error("API Key is missing.");
          }

          const ai = new GoogleGenAI({ apiKey: API_KEY });
          const instruction = PROMPTS[style];

          try {
            const responseStream = await ai.models.generateContentStream({
              model: 'gemini-2.0-flash-lite-preview-02-05',
              contents: [
                {
                  role: 'user',
                  parts: [{ text: `请根据以下素材，进行职场吐槽创作：\n\n${context}` }],
                },
              ],
              config: {
                systemInstruction: instruction,
                temperature: 0.9, 
              },
            });

            let fullText = '';
            for await (const chunk of responseStream) {
              const text = chunk.text();
              if (text) {
                fullText += text;
                onChunk(fullText);
              }
            }
            return fullText;
          } catch (error) {
            console.error("Gemini API Error:", error);
            throw error;
          }
        };

        // ==========================================
        // COMPONENTS
        // ==========================================

        const MarkdownRenderer = ({ content, style, fontSizeClass, fontFamilyClass }) => {
          if (!content) return null;

          const theme = THEMES[style];
          const lines = content.split('\n');
          const formattingRegex = /(\*\*.*?\*\*|\*.*?\*|<u>.*?<\/u>)/g;

          return (
            <div className={`${theme.body} ${fontSizeClass} ${fontFamilyClass}`}>
              {lines.map((line, index) => {
                if (line.startsWith('# ')) {
                  return (
                    <div key={index} className="text-center">
                      <h1 className={theme.h1}>{line.replace('# ', '')}</h1>
                    </div>
                  );
                }
                if (line.startsWith('## ') || line.startsWith('### ')) {
                  return <h3 key={index} className={theme.h2}>{line.replace(/#+\s/, '')}</h3>;
                }
                if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
                   return <li key={index} className={theme.list}>{line.replace(/[-*]\s/, '')}</li>;
                }
                if (line.trim() === '') return <div key={index} className="h-4" />;

                const parts = line.split(formattingRegex);
                return (
                  <p key={index} className={theme.p}>
                    {parts.map((part, i) => {
                      if (part.startsWith('**') && part.endsWith('**')) {
                        return <span key={i} className={theme.highlight}>{part.slice(2, -2)}</span>;
                      }
                      if (part.startsWith('*') && part.endsWith('*')) {
                        return <em key={i} className="italic">{part.slice(1, -1)}</em>;
                      }
                      if (part.startsWith('<u>') && part.endsWith('</u>')) {
                        return <u key={i}>{part.slice(3, -4)}</u>;
                      }
                      return part;
                    })}
                  </p>
                );
              })}
            </div>
          );
        };

        function App() {
          // States
          const [inputContext, setInputContext] = useState(() => localStorage.getItem('roast_input_draft') || '');
          const [selectedStyle, setSelectedStyle] = useState('LITERARY');
          const [resultText, setResultText] = useState('');
          const [loadingState, setLoadingState] = useState('IDLE');
          const [history, setHistory] = useState([]);
          const [showHistory, setShowHistory] = useState(false);
          const [isEditing, setIsEditing] = useState(false);
          const [fontSizeIndex, setFontSizeIndex] = useState(2);
          const [fontFamily, setFontFamily] = useState('default');
          const [currentOverlayMsg, setCurrentOverlayMsg] = useState(LOADING_TEXTS[0]);
          const [currentButtonMsg, setCurrentButtonMsg] = useState("火力装填中...");

          const resultRef = useRef(null);
          const textareaRef = useRef(null);

          // Effects
          useEffect(() => {
            const saved = localStorage.getItem('roast_history');
            if (saved) {
              try {
                setHistory(JSON.parse(saved));
              } catch (e) {
                console.error("Failed to parse history", e);
              }
            }
          }, []);

          useEffect(() => {
            localStorage.setItem('roast_input_draft', inputContext);
          }, [inputContext]);

          useEffect(() => {
            let interval;
            if (loadingState === 'LOADING') {
              let i = Math.floor(Math.random() * LOADING_TEXTS.length);
              setCurrentOverlayMsg(LOADING_TEXTS[i]);
              setCurrentButtonMsg(LOADING_TEXTS[i]);
              
              interval = setInterval(() => {
                i = (i + 1) % LOADING_TEXTS.length;
                const nextMsg = LOADING_TEXTS[i];
                setCurrentOverlayMsg(nextMsg);
                setCurrentButtonMsg(nextMsg);
              }, 3000);
            }
            return () => clearInterval(interval);
          }, [loadingState]);

          // Handlers
          const saveToHistory = (context, result) => {
            const newItem = {
              id: Date.now().toString(),
              context,
              result,
              timestamp: Date.now()
            };
            const newHistory = [newItem, ...history].slice(0, 10); 
            setHistory(newHistory);
            localStorage.setItem('roast_history', JSON.stringify(newHistory));
          };

          const handleRoast = async () => {
            if (!inputContext.trim()) return;
            
            setLoadingState('LOADING');
            setResultText(''); 
            setShowHistory(false);
            setIsEditing(false);

            try {
              const finalContent = await generateRoastStream(inputContext, selectedStyle, (chunk) => {
                setResultText(chunk);
              });
              setLoadingState('SUCCESS');
              saveToHistory(inputContext, finalContent);
            } catch (error) {
              setLoadingState('ERROR');
              setResultText("生成失败：系统被领导的气场震慑住了，请检查 API Key 或稍后再试。");
            }
          };

          const copyToClipboard = () => {
            if (!resultText) return;
            navigator.clipboard.writeText(resultText);
            alert('吐槽文案已复制！快去群里炸场子！');
          };

          const handleShare = async () => {
            if (!resultText) return;
            if (navigator.share) {
              try {
                await navigator.share({
                  title: '职场嘴替 - 深度吐槽',
                  text: resultText,
                });
              } catch (err) {
                if (err.name !== 'AbortError') {
                   console.error('Share failed:', err);
                   copyToClipboard();
                }
              }
            } else {
              copyToClipboard();
            }
          };

          const loadHistoryItem = (item) => {
            setInputContext(item.context);
            setResultText(item.result);
            setLoadingState('SUCCESS');
            setShowHistory(false);
            setIsEditing(false);
          };

          const clearHistory = () => {
            if(confirm("确定要清空所有吐槽记录吗？")) {
                setHistory([]);
                localStorage.removeItem('roast_history');
            }
          }

          const insertFormat = (tagStart, tagEnd) => {
            if (!textareaRef.current) return;
            const textarea = textareaRef.current;
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const text = textarea.value;
            const before = text.substring(0, start);
            const selection = text.substring(start, end);
            const after = text.substring(end);
            
            const newText = before + tagStart + selection + tagEnd + after;
            setResultText(newText);
            
            setTimeout(() => {
                textarea.focus();
                textarea.setSelectionRange(start + tagStart.length, end + tagStart.length);
            }, 0);
          };

          const handleDownloadPDF = async () => {
              if (!resultRef.current) return;
              const element = resultRef.current;
              
              try {
                  const canvas = await html2canvas(element, {
                      scale: 2,
                      useCORS: true,
                      logging: false,
                      backgroundColor: null
                  });
                  
                  const imgData = canvas.toDataURL('image/png');
                  const pdfWidth = canvas.width;
                  const pdfHeight = canvas.height;
                  
                  const pdf = new jsPDF({
                      orientation: pdfWidth > pdfHeight ? 'l' : 'p',
                    
