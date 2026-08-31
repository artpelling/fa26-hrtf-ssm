\usepackage{tikz}
\usepackage{pgfplots}

\usetikzlibrary{calc}
\usetikzlibrary{patterns}

\ProvidesClass{tub-beamer}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions\relax
\LoadClass[xcolor=table,hyperref={bookmarks},9pt,t,aspectratio=169]{beamer} % pdfpagemode=FullScreen
%\RequirePackage[scaled=0.85]{helvet}
\RequirePackage{xspace}
\RequirePackage{etoolbox}

\setlength{\unitlength}{1mm}
\newlength{\rand}
\setlength{\rand}{5mm}

% 160 mm x 90 mm

\xdefinecolor{TU-rot}{RGB}{168,29,30} % nicht das corporate rot, sondern das des logos!
\xdefinecolor{TU-hellgrau}{RGB}{178,178,178}
\xdefinecolor{TU-dunkelgrau}{RGB}{67,67,67}

\setbeamersize{text margin left=\rand, text margin right=\rand}

\newcommand*{\lengthinmm}[1]{\strip@pt\dimexpr0.351459804\dimexpr#1\relax\relax}
\newcommand{\smallcirc}{\begin{picture}(2,2)\put(1,0.9){\circle*{0.88}}\end{picture}}
\newcommand{\pagename}{Seite} % Definition wird vom babel-Paket ueberschrieben

\linespread{1.1}
\newcommand{\leer}{}
\newcommand{\pathtomylogo}{}

\setbeamertemplate{title page}{%
  \thispagestyle{empty}
  \vspace{-\headheight}
  \hspace{-\rand}%
  \begin{picture}
    (100,93.6)
    \put(125,74){\includegraphics[width=30mm]{logos/TU-lang}}
    \put(-0.5,32){\color{TU-rot}\rule{\rand}{40mm}}
    \put(5,32){\includegraphics[height=40mm,width=150mm]{logos/rar}}
    \put(5,8){\parbox[b][23mm][s]{150mm}{%
      \raggedright\vfill
      \usebeamerfont{title}\usebeamercolor[fg]{titlelike}{\inserttitle\par}
      \vfill
      \color{TU-dunkelgrau}\fontsize{8pt}{8pt}\selectfont\insertauthor%
      \ifdefempty{\insertinstitute}{}{~\textbar~\insertinstitute}%
      \ifdefempty{\insertsubtitle}{}{~\textbar~\insertsubtitle}\par%
      \vfill%
    }}
    \put(5,10.95){\color{TU-hellgrau}{\rule{150mm}{0.5pt}}}
  \end{picture}
}

\setbeamertemplate{headline}{%
  \begin{picture}
    (100,16)
    \put(135,1){\includegraphics[width=20mm]{logos/TU-kurz}}
  \end{picture}
}

\setbeamertemplate{frametitle}{%
  \vspace{-10.5mm}
  \insertframetitle
  \vspace{-1mm}
}

\def\progressbar{}  % the progress bar

\newcount\tmpcounta % auxiliary counter
\newcount\tmpcountb % auxiliary counter
\newdimen\pbht % progressbar height
\newdimen\xmax % position of page number
\newdimen\tmpdim % auxiliary dimension
\newdimen\xmin % auxiliary dimension
\newdimen\xdif % progressbar width
\newdimen\xnum      % pos of number

\xmin = 0.8\linewidth
\xdif = 0.255\linewidth
\xmax = 1.055\linewidth
\xnum = 1.065\linewidth
\pbht= 0.4pt

% the progress bar
\def\progressbar{
  \tmpcounta=\insertframenumber
  \tmpcountb=\inserttotalframenumber
  \tmpdim=\xdif
  \multiply\tmpdim by \tmpcounta
  \divide\tmpdim by \tmpcountb
  \advance\tmpdim by \xmin

  \begin{tikzpicture}[very thin, baseline=-2.6cm]%-0.6ex
    \node at (0pt, 0pt) {};
    \filldraw[draw=none,fill=TU-hellgrau]
    (\xmin,  1.7pt) rectangle (\xmax, 2.3pt);
    \filldraw[draw=none,fill=TU-dunkelgrau]
    (\tmpdim, 2pt) circle [radius=1.1pt];
    \node at (\xnum,2pt) {\insertframenumber};
  \end{tikzpicture}%
}

\setbeamertemplate{footline}{%
  \begin{picture}
    (100,5)
    \put(5,5){\color{TU-hellgrau}\rule{150mm}{0.5pt}}
    \put(5,2.5){\parbox[b][6mm][s]{150mm}{\fontsize{5pt}{5pt}\selectfont
      \raggedright\vfill
      \textbf{\insertshorttitle}~\textbar~\insertshortauthor
      \ifdefempty{\grant}{}{~\textbar~\grant}
    }}
    \put(5,-2){\parbox[b][6mm][s]{150mm}
      \progressbar
    }
    \put(123,1){\ifx\pathtomylogo\leer
      \else{\makebox[0mm][r]{\includegraphics[height=6mm]{\pathtomylogo}}}
      \fi
    }
  \end{picture}
}

\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{background}{}
\setbeamertemplate{itemize item}[triangle]
\setbeamertemplate{itemize subitem}{\smallcirc}
\setbeamertemplate{itemize subsubitem}{\frqq}

\setbeamercolor{alerted text}{fg=TU-rot}
\setbeamercolor{block body}{bg=TU-hellgrau}
\setbeamercolor{block body alerted}{bg=TU-dunkelgrau}
\setbeamercolor{block title}{bg=TU-rot,fg=white}
\setbeamercolor{block title alerted}{bg=TU-rot,fg=white}
\setbeamercolor{block title example}{bg=TU-rot,fg=white}
\setbeamercolor{frametitle}{fg=TU-rot}
\setbeamercolor{item}{fg=black}
\setbeamercolor{navigation symbols}{fg=TU-dunkelgrau}
\setbeamercolor{section in toc}{fg=TU-rot}
\setbeamercolor{titlelike}{fg=TU-rot}
\setbeamercolor{footline}{fg=TU-dunkelgrau}
\setbeamercolor{itemize item}{fg=TU-rot}

\setbeamerfont{block title}{size=\normalsize}
\setbeamerfont{block title alerted}{size=\normalsize}
\setbeamerfont{block title example}{size=\normalsize}
\setbeamerfont{titlelike}{}
\setbeamerfont{title}{size=\fontsize{14}{16}\selectfont}
\setbeamerfont{title in head}{series=\bfseries}
\setbeamerfont{frametitle}{size=\LARGE}
\setbeamerfont{section in toc}{series=\bfseries}

\setbeamerfont*{itemize/enumerate body}{parent=normal text}
\setbeamerfont*{itemize/enumerate subbody}{parent=itemize/enumerate body}
\setbeamerfont*{itemize/enumerate subsubbody}{parent=itemize/enumerate body}

\renewcommand{\emph}{\textbf}
\renewcommand{\ttdefault}{lmtt}
\newcommand{\fazit}[1]{{\color{TU-rot}#1}\xspace}

\AtBeginEnvironment{theorem}{%
  \setbeamercolor{block title}{use=theorem,fg=white,bg=TU-rot}
  \setbeamercolor{block body}{parent=normal text,use=theorem,bg=bg!90!black}
}
