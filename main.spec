# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\project\\env\\paddleocr\\Lib\\site-packages\\paddle\\libs', 'D:\\project\\env\\paddleocr\\Lib\\site-packages\\paddleocr', 'D:\\project\\env\\paddleocr\\Lib\\site-packages\\paddleocr\\ppocr\\utils\\e2e_utils', 'D:\\project\\env\\paddleocr\\Lib\\site-packages\\paddleocr\\ppstructure\\table', 'E:\\temp\\screen'],
             binaries=[('D:\\project\\env\\paddleocr\\Lib\\site-packages\\paddle\\libs', '.')],
             datas=[('E:\\temp\\screen\\bitbug_favicon.ico', '.'), ('D:\\project\\env\\paddleocr\\Lib\\site-packages\\paddleocr\\ppocr\\utils\\ppocr_keys_v1.txt', '.\\ppocr\\utils'), ('D:\\project\\env\\paddleocr\\Lib\\site-packages\\paddleocr\\ppocr\\utils\\dict\\table_structure_dict.txt', '.\\ppocr\\utils\\dict')],
             hiddenimports=['extract_textpoint_slow', 'tablepyxl', 'tablepyxl.style'],
             hookspath=['.'],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['matplotlib'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='bitbug_favicon.ico')
