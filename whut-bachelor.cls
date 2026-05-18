%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% UNOFFICIAL LaTeX Template for WHUT Bachelor Thesis
%% First Released on 2019/09/29
%% Created by Huang Yuxi
%% See https://github.com/huangyxi/WHUT-Bachelor
%% ========== 人工修改：适配结课作业 ==========
%% 1.删除：原创声明、版权授权、英文摘要、致谢
%% 2.修改：封面+页眉为 武汉理工大学结课作业
%% 3.新增：左上角序号、学号，以及居中的课程名称
%% 4.重构：将底层引用引擎由 biblatex 替换为 BibTeX(gbt7714)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{whut-bachelor}
[2022/05/17 v0.99991 Unofficial LaTeX Document Class for WHUT Bachelor Thesis]

\newcommand*\whut@tokens@title{}
\newcommand*\whut@tokens@school{}
\newcommand*\whut@tokens@class{}
\newcommand*\whut@tokens@author{}
\newcommand*\whut@tokens@supervisor{}
\newcommand*\whut@tokens@keywords{}
% ========== 新增变量定义 ==========
\newcommand*\whut@tokens@serialnumber{}
\newcommand*\whut@tokens@studentid{}
\newcommand*\whut@tokens@coursename{}

\newif\ifwhut@options@minimal\whut@options@minimalfalse
\newif\ifwhut@options@nobib\whut@options@nobibfalse
\newif\ifwhut@options@heitipatch\whut@options@heitipatchfalse

\DeclareOption{minimal}{\whut@options@minimaltrue}	% only load fundamental packages
\DeclareOption{nobib}{\whut@options@nobibtrue}	% do NOT load biblatex
\DeclareOption{noextrafonts}{
	\ClassWarning{whut-bachelor}{the `noextrafonts' is deprecated, and it now can be detected automatically}
}	% do NOT use SinoType(R) fonts: STzhongsong (DEPRECATED)
\DeclareOption{heitipatch}{\whut@options@heitipatchtrue}	% patch for a latex3 bug to make `heiti' as bold text
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexart}}
%\ExecuteOptions{doctor,chinese,print,super}
\ProcessOptions\relax

\ifwhut@options@minimal
\whut@options@nobibtrue
\fi

\RequirePackage{ifxetex}
\RequireXeTeX
\PassOptionsToPackage{quiet}{xeCJK}
\xeCJKsetup{PunctStyle=kaiming}

\LoadClass[a4paper, 12pt]{ctexart}
\ifwhut@options@minimal\whut@options@nobibtrue\fi


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% load packages

\RequirePackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Arial}
\IfFontExistsTF{STZhongsong}{
	\providecommand{\zhongsong}{\CJKfontspec{STZhongsong}}
}{
	\IfFontExistsTF{STZhongsong.ttf}{
		\providecommand{\zhongsong}{\CJKfontspec{STZhongsong.ttf}}
	}{
		\ClassWarning{whut-bachelor}{There is NO font `STZhongsong' in your enviroment. you should install it to meet the requirements.}
		\providecommand{\zhongsong}{\songti}
	}
}

\ifwhut@options@heitipatch
\IfFontExistsTF{SimSun}{
	\setCJKmainfont{SimSun}[BoldFont={SimHei}, ItalicFont={SimKai}]
}{
	\setCJKmainfont{FandolSong}[BoldFont={FandolHei}, ItalicFont={FandolKai}]
}
\fi

\RequirePackage{amsmath, amsfonts}
\RequirePackage[includeheadfoot]{geometry}
\geometry{
	top=2.5cm, bottom=2cm, left=2.5cm, right=2cm,
	headheight=13pt, headsep=0.1cm, footskip=0.51cm
}	% footskip should be 0.4cm, but this is too small
\RequirePackage[indentafter]{titlesec}	% \titlespacing*
\RequirePackage{fancyhdr}
\RequirePackage{titletoc}

% ========== 核心修改：使用 gbt7714 宏包处理参考文献 ==========
\ifwhut@options@nobib\else
\RequirePackage[sort&compress]{gbt7714}
\fi

\ifwhut@options@minimal\else
\RequirePackage{amssymb}
\RequirePackage{bm}
\RequirePackage{enumitem}
\setlist[1]{parsep=0ex, topsep=1ex, itemsep=0ex}
\RequirePackage{xcolor}
\RequirePackage{graphicx}
\RequirePackage{array, longtable, booktabs}
\RequirePackage{multirow, bigstrut, bigdelim}
\RequirePackage{caption, subcaption}
\captionsetup{labelsep = quad}
\captionsetup[figure]{skip = {5pt plus 2pt minus 1pt}}
\RequirePackage{cprotect}
\RequirePackage{listings}
\RequirePackage{pdfpages}
\fi

\RequirePackage{hyperref}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% define markups

\widowpenalty=10000
\clubpenalty=10000

\setlength{\baselineskip}{20pt}
\renewcommand\normalsize{%
	\abovedisplayskip 6\p@ \@plus2\p@ \@minus4\p@	
	\abovedisplayshortskip \z@ \@plus3\p@%
	\belowdisplayshortskip 7\p@ \@plus3\p@ \@minus4\p@%
	\belowdisplayskip \abovedisplayskip%
	\let\@listi\@listI%
}
\titlespacing*{\section}{0pt}{0.5\baselineskip}{0.5\baselineskip}
\titlespacing*{\subsection}{0pt}{0.5\baselineskip}{0.5\baselineskip}
\titlespacing*{\subsubsection}{0pt}{0.5\baselineskip}{0.5\baselineskip}

\hypersetup{
	pdfstartview=FitH,
	CJKbookmarks=true,
	bookmarksnumbered=true,
	bookmarksopen=true,
	colorlinks=true,
	allcolors=black,
	pdfsubject={WHUT Coursework},
	pdfcreator={whut-bachelor class Modified for Coursework},
}

{\sf}	
\renewcommand{\maketitle}{\par
	\begingroup
	\global\@topnum\z@	
	\pdfbookmark[1]{封面}{anchor}
	\@maketitle
	\endgroup
	\global\let\thanks\relax
	\global\let\maketitle\relax
	\global\let\@maketitle\relax
	\global\let\@thanks\@empty
	\global\let\@author\@empty
	\global\let\@date\@empty
	\global\let\@title\@empty
	\global\let\title\relax
	\global\let\author\relax
	\global\let\date\relax
	\global\let\and\relax
}

% ========== 核心修改：调整封面排版 ==========
\renewcommand{\@maketitle}{%
	\thispagestyle{empty}
	% 左上角的序号和学号
	\begin{flushleft}
		\zihao{4} 
		序号：\whut@tokens@serialnumber \\
		学号：\whut@tokens@studentid
	\end{flushleft}
	
	\vspace*{0.5cm} 
	\begin{center}
		{\zihao{1}\zhongsong \whut@cap@titlename} \\
		\vspace*{3.3cm}
		{\zihao{2}\bfseries \whut@tokens@title}\\
		\vspace*{4cm} 
		\zhongsong
		\begin{tabular}{cc}
			\zihao{-2} 学院（系）：&\underline{\makebox[7cm][c]{\zihao{-2}\whut@tokens@school}} \\
			\\
			\zihao{-2}专业班级: & \underline{\makebox[7cm][c]{\zihao{-2}\whut@tokens@class}} \\
			\\
			\zihao{-2}课程名称: & \underline{\makebox[7cm][c]{\zihao{-2}\whut@tokens@coursename}} \\
			\\
			\zihao{-2}学生姓名: & \underline{\makebox[7cm][c]{\zihao{-2}\whut@tokens@author}} \\
			\\
			\zihao{-2}指导教师: & \underline{\makebox[7cm][c]{\zihao{-2}\whut@tokens@supervisor}} \\
			\\
		\end{tabular}
	\end{center}
	\clearpage
}

\renewenvironment{abstract}{%
	\section*{\pdfbookmark[1]{\whut@cap@zhabstractname}{zhabstract}\whut@cap@zhabstractname}
	\pagenumbering{Roman}
	\quotation
	\pagestyle{plain}
}{%
	\thispagestyle{plain}
	\endquotation
	\clearpage
}

\newenvironment{enabstract}{%
	\section*{\pdfbookmark[1]{\whut@cap@enabstractname}{enabstract}\whut@cap@enabstractname}
	\quotation
	\pagestyle{plain}
}{%
	\thispagestyle{plain}
	\endquotation
	\clearpage
}

\renewenvironment{quotation}
{\list{}{\listparindent 2em
		\itemindent \listparindent
		\rightmargin\z@
		\leftmargin\z@
		\parsep \z@ \@plus\p@}
	\item\relax}
{\endlist}

%% define toc style
\titlecontents{section}[0pt]{\mdseries}
{\thecontentslabel\hskip.5em}{}{\titlerule*[0.5pc]{.}\contentspage}
\titlecontents{subsection}[4ex]{\mdseries}
{\thecontentslabel\hskip.5em}{}{\titlerule*[0.5pc]{.}\contentspage}
\titlecontents{subsubsection}[8ex]{\mdseries}
{\thecontentslabel\hskip.5em}{}{\titlerule*[0.5pc]{.}\contentspage}

\numberwithin{equation}{section}
\numberwithin{table}{section}
\numberwithin{figure}{section}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\zihao{5} \whut@cap@titlename}
\fancyfoot[C]{\zihao{5} \thepage}
\renewcommand{\headrulewidth}{0.65pt}

\fancypagestyle{plain}{%
	\fancyhf{}
	\fancyhead[C]{\zihao{5} \whut@cap@titlename}
	\fancyfoot[C]{\zihao{5} \thepage}
	\renewcommand{\headrulewidth}{0.65pt}
}

\setcounter{secnumdepth}{3}

\ctexset{
	section = {
		format = \centering\bfseries\zihao{-2},
		numberformat = \mdseries\sffamily,
		name = {第, 章},
	},
	subsection = {
		format = \bfseries\zihao{3},
		numberformat = \mdseries\sffamily,
	},
	subsubsection = {
		format = \bfseries\zihao{4},
		numberformat = \mdseries\sffamily,
	},
	appendix = {
		name = 附录,
	}
}

\let\@tableofcontents\tableofcontents
\renewcommand{\tableofcontents}{%
	\clearpage
	\begingroup
	\pagestyle{plain}
	\pdfbookmark[1]{\whut@cap@contentsname}{contents}
	\@tableofcontents
	\endgroup
	\thispagestyle{plain}
	\clearpage
	\pagenumbering{arabic}
	\let\@tableofcontents\relex
}

\RequirePackage{pifont}
\RequirePackage[symbol*,stable]{footmisc}
\DefineFNsymbols{circled}{{\ding{192}}{\ding{193}}{\ding{194}}{\ding{195}}%
	{\ding{196}}{\ding{197}}{\ding{198}}{\ding{199}}{\ding{200}}{\ding{201}}}
\setfnsymbol{circled}

%% redefine appendix
\let\@appendix\appendix
\renewcommand\appendix{\par
	\@appendix
	\gdef\thesubsection{\appendixname\Alph{section}\@arabic\c@subsection}
	\gdef\thesubsubsection{\appendixname\Alph{section}\arabic{subsection}.\@arabic\c@subsubsection}
	\renewcommand\thefigure{\Alph{section}\arabic{figure}}
	\renewcommand\thetable{\Alph{section}\arabic{table}}
	\renewcommand\theequation{A\arabic{equation}}
	\let\@appendix\relex
}

%% rename caption names
\renewcommand\contentsname{\whut@cap@contentsname}
\renewcommand\listfigurename{\whut@cap@listfigurename}
\renewcommand\listtablename{\whut@cap@listtablename}
\renewcommand\indexname{\whut@cap@indexname}
\renewcommand\figurename{\whut@cap@figurename}
\renewcommand\tablename{\whut@cap@tablename}
\renewcommand\appendixname{\whut@cap@appendixname}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% define commands

\renewcommand*\title[1]{\renewcommand{\whut@tokens@title}{#1}\hypersetup{pdftitle={#1}}}
\newcommand*\school[1]{\renewcommand{\whut@tokens@school}{#1}}
\newcommand*\class[1]{\renewcommand{\whut@tokens@class}{#1}}
\renewcommand*\author[1]{\renewcommand{\whut@tokens@author}{#1}\hypersetup{pdfauthor={#1}}}
\newcommand*\supervisor[1]{\renewcommand{\whut@tokens@supervisor}{#1}}
% ========== 新增命令定义 ==========
\newcommand*\serialnumber[1]{\renewcommand{\whut@tokens@serialnumber}{#1}}
\newcommand*\studentid[1]{\renewcommand{\whut@tokens@studentid}{#1}}
\newcommand*\coursename[1]{\renewcommand{\whut@tokens@coursename}{#1}}

%% define keywords & enkeywords
\newcommand\keywords[1]{%
	\vspace{\baselineskip}
	{\noindent\zihao{4}\bfseries\whut@cap@keywordsname：}~{\zihao{-4} #1}
	\hypersetup{pdfkeywords={#1}}
}

\newcommand\enkeywords[1]{%
	\vspace{\baselineskip}
	{\noindent\zihao{4}\bfseries\whut@cap@enkeywordsname：}~{\zihao{-4} #1}
}

% ========== 核心修改：完美适配武理规范的参考文献样式 ==========
\ifwhut@options@nobib\else
\let\whut@oldbibliography\bibliography
\renewcommand{\bibliography}[1]{%
	\clearpage
	\phantomsection
	\addcontentsline{toc}{section}{\whut@cap@refname} 
	\begingroup
	\zihao{5} 
	\bibliographystyle{gbt7714-numerical} 
	\whut@oldbibliography{#1}
	\endgroup
}
\fi


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% define enviroments

\ifwhut@options@minimal\else
\newtheorem{conjecture}{\whut@cap@conjecture}
\newtheorem{proposition}{\whut@cap@proposition}
\newtheorem{assumption}{\whut@cap@assumption}
\newtheorem{definition}{\whut@cap@definition}
\newtheorem{axiom}{\whut@cap@axiom}
\newtheorem{lemma}{\whut@cap@lemma}
\newtheorem{theorem}{\whut@cap@theorem}
\newtheorem{principle}{\whut@cap@principle}
\newtheorem{conclusion}{\whut@cap@conclusion}
\newtheorem{corollary}{\whut@cap@corollary}
\newtheorem{example}{\whut@cap@example}
\newtheorem{solution}{\whut@cap@solution}
\newtheorem{proof}{\whut@cap@proof}
\newtheorem{property}{\whut@cap@property}
\newtheorem{remark}{\whut@cap@remark}
\fi


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% define constants
% ========== 核心修改：全局标题改为 武汉理工大学结课作业 ==========
\newcommand*{\whut@cap@zhabstractname}{摘~~要}
\newcommand*{\whut@cap@enabstractname}{Abstract}
\newcommand*{\whut@cap@keywordsname}{关键词}
\newcommand*{\whut@cap@enkeywordsname}{Key words}
\newcommand*{\whut@cap@titlename}{武汉理工大学课程设计(论文)}
\newcommand*{\whut@cap@contentsname}{目~~录}
\newcommand*{\whut@cap@listfigurename}{插图清单}
\newcommand*{\whut@cap@listtablename}{附表清单}
\newcommand*{\whut@cap@refname}{参考文献}
\newcommand*{\whut@cap@indexname}{索引}
\newcommand*{\whut@cap@figurename}{图}
\newcommand*{\whut@cap@tablename}{表}
\newcommand*{\whut@cap@appendixname}{附}

\newcommand*{\whut@cap@conjecture}{猜想}
\newcommand*{\whut@cap@proposition}{命题}
\newcommand*{\whut@cap@assumption}{假设}
\newcommand*{\whut@cap@definition}{定义}
\newcommand*{\whut@cap@axiom}{公理}
\newcommand*{\whut@cap@lemma}{引理}
\newcommand*{\whut@cap@theorem}{定理}
\newcommand*{\whut@cap@principle}{定律}
\newcommand*{\whut@cap@conclusion}{结论}
\newcommand*{\whut@cap@corollary}{推论}
\newcommand*{\whut@cap@example}{例}
\newcommand*{\whut@cap@solution}{解}
\newcommand*{\whut@cap@proof}{证明}
\newcommand*{\whut@cap@property}{性质}
\newcommand*{\whut@cap@remark}{注解}

\endinput