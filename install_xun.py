import os
try:
    import maya.mel as mel
    import maya.cmds as cmds
    isMaya = True
except ImportError:
    isMaya = False
def onMayaDroppedPythonFile(*args, **kwargs):
    """This function is only supported since Maya 2017 Update 3"""
    pass

srcPath = os.path.join(os.path.dirname(__file__) , 'xun_tool_UI.py')
srcPath = os.path.normpath(srcPath)
iconPath = os.path.join(os.path.dirname(__file__) , 'xun_icon.png')
print(srcPath)

shelf = mel.eval('$gShelfTopLevel=$gShelfTopLevel')
parent = cmds.tabLayout(shelf, query=True, selectTab=True)
cmds.shelfButton(
    command = srcPath + '.build_xun_tool_UI',
    annotation='TH RIGsd TOOLS',
    sourceType='Python',
    image= iconPath,
    parent=parent
)
