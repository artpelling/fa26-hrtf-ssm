% Latex Paper Template for FA2026
%
% !!! DO NOT MODIFY THIS FILE !!!!

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fa2026}[2025/11/04 Conference Template]

% Inherit from 10pt article class
\LoadClass[10pt]{article}

%%%<<<<<<<<<<>>>>>>>>>>>%%%
%%%TO BE CHANGED EVERY YEAR
\newcommand{\conferenceedition}{12\textsuperscript{th}}
\newcommand{\conferencedate}{8\textsuperscript{th} -- 12\textsuperscript{th} September}
\newcommand{\conferenceyear}{2026}
%%%<<<<<<<<<<>>>>>>>>>>>%%%

%% Definition of used packages
\RequirePackage{lmodern}
\RequirePackage{microtype}
\RequirePackage[utf8]{inputenc}
\RequirePackage[english]{babel}
\RequirePackage{csquotes}
\RequirePackage{titlesec}
\RequirePackage[font=small, labelfont=bf]{caption} % Formatting of captions
\captionsetup[table]{skip=0pt} % Adjust '5pt' to your desired space
\RequirePackage{fancyhdr}
\RequirePackage{setspace} % Better line spacing control
\RequirePackage{authblk} % For authors and affiliations
\RequirePackage[
    style=ieee,
    citestyle=numeric-comp,
    sortcites=true,
    backend=biber]{biblatex}
\RequirePackage[bottom=3.5cm, top=2cm, left=2cm, right=2cm, a4paper]{geometry}
\RequirePackage{xkeyval}
\RequirePackage{amsmath, amssymb}
\RequirePackage{graphicx}
\RequirePackage{siunitx}
\RequirePackage{xcolor}
\RequirePackage{url}
\RequirePackage[
    colorlinks=true,
    linkcolor=black,
    citecolor=black,
    urlcolor=black,
    pdfborder={0 0 0}
]{hyperref}
\pdfstringdefDisableCommands{%
  \def\textsuperscript#1{#1}%
}
\RequirePackage[capitalize]{cleveref}

\definecolor{blueAcoustics}{HTML}{3977aa}

% Set up options
\newcommand{\FAreview}{nonpeer} % default
\DeclareOptionX{peer-review}{\renewcommand{\FAreview}{peer}}
\DeclareOptionX{non-peer-review}{\renewcommand{\FAreview}{nonpeer}}

% Process options
\ProcessOptionsX\relax

% Helper commands for conditional checks
\def\@peer{peer}
\def\@nonpeer{nonpeer}

\newcommand{\@correspondingemail}{}
\newcommand{\@correspondingname}{}
\newcommand{\correspondingauthor}[2]{%
  \renewcommand{\@correspondingemail}{#1}%
  \renewcommand{\@correspondingname}{#2}%
}

%% Keywords command
\newcommand{\@keywords}{}  % Store keywords internally (plain text for PDF)
\providecommand{\keywords}[1]
{%
  \renewcommand{\@keywords}{#1}% Store plain keywords for PDF metadata
  \noindent
  \parbox{\linewidth}
  {%
    \small	
    \textbf{Keywords:} \itshape#1%
  }%
}

%% Set column separation
\setlength{\columnsep}{8mm}

%% Configure section titles
\titleformat{\section}{\large\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\bfseries}{\thesubsection.}{0.5em}{}
\titleformat{\subsubsection}{\itshape}{\thesubsubsection.}{0.5em}{}
\titleformat{\paragraph}{\bfseries}{\theparagraph.}{0.5em}{}
\titleformat{\subparagraph}{\bfseries}{\thesubparagraph.}{0.5em}{}

% Adjust spacing: {left}{before}{after}
\titlespacing*{\section}{0pt}{8pt}{1pt}
\titlespacing*{\subsection}{0pt}{6pt}{1pt}
\titlespacing*{\subsubsection}{0pt}{4pt}{1pt}
\titlespacing*{\paragraph}{0pt}{4pt}{1pt}
\titlespacing*{\subparagraph}{0pt}{3pt}{1pt}

\setstretch{0.95}  % Adjust between 0.8-1.0 for tighter/looser spacing
\setlength\parindent{0pt}

\twocolumn

%% Configure header and footer
\pagestyle{fancy}

\fancyhf{} % Clear all header and footer fields
\fancyhead{} % Explicitly clear header

\renewcommand{\headrulewidth}{0pt} % Remove header rule
\renewcommand{\footrulewidth}{0pt} % Remove footer rule
\setlength{\footskip}{43pt}  

\lfoot{%
  \raisebox{-.7cm}{%
    \ifthenelse{\equal{\FAreview}{peer}}{%
      \href{https://euracoustics.org/}{\includegraphics[height=1.36cm]{assets/footer_logo_eaa.jpg}}%
    }{%
      \href{https://euracoustics.org/}{\includegraphics[height=1.36cm]{assets/footer_logo_eaa_bw}}%
    }%
  }%
}

\rfoot{%
  \raisebox{-.7cm}{%
    \ifthenelse{\equal{\FAreview}{peer}}{%
      \href{http://aaa-oega.org/}{\includegraphics[height=1.36cm]{assets/footer_logo_oega.jpg}}%
    }{%
      \href{http://aaa-oega.org/}{\includegraphics[height=1.36cm]{assets/footer_logo_oega_bw.jpg}}%
    }%
  }%
}

\cfoot{
  \textcolor{black}{\fontsize{10}{10}\selectfont \textbf{\conferenceedition\ Convention of the European Acoustics Association}}\\%
  \textcolor{black}{\fontsize{9}{9}\selectfont Graz, Austria \textbullet \ \conferencedate\ \conferenceyear \ \textbullet \hspace{22pt}}%
}

%% Title section
% Configure title formatting
\renewcommand{\maketitle}{%
  \twocolumn[%
    \begin{center}
      % Banner/logo
      \vspace{-2cm}
      \ifthenelse{\equal{\FAreview}{peer}}{%
        \includegraphics[width=12.5cm]{assets/fa26_banner_light_rgb}\\%
      }{%
        \includegraphics[width=12.5cm]{assets/fa26_banner_white_rgb}\\%
      }%
      \vspace{0.5cm}
      
      % Title: bold, uppercase, Large
      {\Large\bfseries\MakeUppercase{\@title}\par}
      \vskip 1em
      
      % Authors: large size
      {\large\@author\par}
      \vskip 1em
 
      % Peer review notice
      \parbox{\textwidth}{%
        \footnotesize%
        \setlength{\baselineskip}{7pt}%
        \selectfont%
        \ifthenelse{\equal{\FAreview}{peer}}{%
          \centering This paper is a revised version of the authors' submitted manuscript that was peer-reviewed by at least two anonymous reviewers.%
        }{%
          This contribution has been accepted based on the submitted abstract. The submitted manuscript was not reviewed and is reproduced here without edits or corrections by the conference board. Neither the EAA nor the AAA take responsibility for its contents.
        }%
      }
      \vskip 2em
    \end{center}
  ]%
  % Add footnotes for corresponding author and copyright (bypass hyperref)
  \bgroup
  \def\@thefnmark{}% Empty footnote mark
  \def\@makefnmark{}% Don't print mark
  \long\def\@makefntext##1{##1}% Just print text
  \insert\footins{%
    \reset@font\footnotesize
    \interlinepenalty\interfootnotelinepenalty
    \splittopskip\footnotesep
    \splitmaxdepth \dp\strutbox \floatingpenalty \@MM
    \hsize\columnwidth \@parboxrestore
    \noindent
    \textit{\textbf{Corresponding author}: \href{mailto:\@correspondingemail}{\@correspondingemail}.}\strut\par
    \itshape\textbf{Copyright}: \textcopyright\conferenceyear\ \@correspondingname{} This is an open-access article distributed under the terms of the Creative Commons Attribution 3.0 Unported License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited.\strut
  }%
  \egroup
  % Set PDF metadata after maketitle
  \hypersetup{%
    pdftitle={\@title},
    pdfauthor={\@correspondingname},
    pdfsubject={Forum Acusticum \conferenceyear},
  }%
}

% Configure authblk formatting
\renewcommand\Authfont{\large\normalfont}         % Authors in \large, normal weight
\renewcommand\Affilfont{\normalsize\itshape}      % Affiliations in normal size, italic
\renewcommand\Authsep{, }                          % Separator between authors (comma-space)
\renewcommand\Authand{, }                          % Separator before last author
\renewcommand\Authands{, }                         % Separator before last author (more than 2)
\setlength{\affilsep}{0.5em}                       % Space between affiliation blocks

% Remove date
\date{}

%% Abstract environment
\renewenvironment{abstract}{%
  \begin{center}
    {\large\bfseries Abstract}
  \end{center}
  \vspace{-8pt}%
  \begingroup
  \setlength{\parindent}{0pt}
}{%
  \endgroup
  \par\vspace{.8em}%
}

\endlist
\def\title#1{\gdef\@title{{#1}}}
\newif\if@saspsection

\flushbottom
\sloppy % for improved formatting
