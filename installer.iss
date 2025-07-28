[Setup]
AppName=WeChatDaemon
AppVersion=1.0
DefaultDirName={pf}\WeChatDaemon
DisableDirPage=yes
DefaultGroupName=WeChatDaemon
OutputBaseFilename=WeChatDaemon_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\WeChatDaemon_Setup.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\WeChatDaemon_Config.exe"; DestDir: "{app}"; DestName: "config_gui.exe"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\配置企业微信推送"; Filename: "{app}\config_gui.exe"
Name: "{commondesktop}\配置企业微信推送"; Filename: "{app}\config_gui.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\WeChatDaemon_Setup.exe"; Parameters: "install"; Flags: runhidden
Filename: "{app}\WeChatDaemon_Setup.exe"; Parameters: "start"; Flags: runhidden waituntilterminated

[UninstallRun]
Filename: "{app}\WeChatDaemon_Setup.exe"; Parameters: "stop"; Flags: runhidden waituntilterminated
Filename: "{app}\WeChatDaemon_Setup.exe"; Parameters: "remove"; Flags: runhidden waituntilterminated
