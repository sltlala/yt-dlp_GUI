````
MyDownloadTool/
├── app/
│   ├── __init__.py  # 初始化文件，使app成为包
│   ├── main.py       # 主程序入口，启动窗口等
│   ├── models/       # 数据模型与数据库交互
│   │   ├── __init__.py
│   │   ├── db_manager.py  # SQLite3数据库管理模块
│   │   └── download_task.py  # 下载任务模型
│   ├── services/     # 核心服务层
│   │   ├── __init__.py
│   │   ├── download_manager.py  # 使用yt-dlp和aria2的下载管理器
│   │   └── aria2_config.py  # aria2配置相关
│   ├── ui/           # 用户界面相关
│   │   ├── __init__.py
│   │   ├── main_window.py  # PySide6主窗口类
│   │   ├── widgets/        # UI组件（如任务列表、设置窗口等）
│   │   │   ├── task_list_widget.py
│   │   │   └── settings_dialog.py
│   │   └── resources/      # 界面图标、样式表等资源文件
│   │       ├── icons/
│   │       └── stylesheets/
│   ├── utils/         # 工具函数或辅助类
│   │   ├── __init__.py
│   │   └── helper_functions.py
│   └── constants.py    # 常量定义
├── config/            # 应用配置文件夹
│   ├── aria2.conf     # aria2配置文件
│   └── app_settings.json  # 应用内部设置文件
├── logs/              # 日志文件夹
├── requirements.txt   # 依赖库清单
├── README.md          # 项目说明文档
├── LICENSE            # 许可证文件
└── setup.py           # 包打包和安装脚本
````
````
MyDownloadTool/
├── app/
│   ├── __init__.py
│   ├── launcher.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── download_task.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── download_manager.py
│   │   │   └── aria2_config.py
│   │   ├── ui/
│   │   │   ├── __init__.py
│   │   │   ├── main_window.py
│   │   │   ├── widgets/
│   │   │   │   ├── __init__.py
│   │   │   │   └── task_list_widget.py
│   │   │   └── resources/
│   │   │       ├── icons/
│   │   │       └── stylesheets/
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helper_functions.py
│   └── app_constants.py
├── config/
│   ├── dev/
│   │   ├── aria2.conf
│   │   └── app_settings.json
│   ├── test/
│   └── prod/
├── logs/
├── requirements.txt
├── README.md
├── LICENSE
└── setup.py
````
