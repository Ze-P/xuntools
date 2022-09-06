import maya.mel as mel
import maya.cmds as zx
import maya.cmds as mc
from maya import cmds
#重名工具
def double_nameadd(name):
    
    list = [str(r) for r in zx.ls(ap = 1)]


    n = 0
    check_back = name

    # 这里做检测后建立总组
    while check_back in list:
        n = n + 1
        k = name
        check_back = '%s' % name + '%s' % n
    return check_back


#选择储存器
def select_stroer(arg):
    select_list_nows = zx.ls(sl=1)
    zx.textScrollList(select_list , edit = 1 , ra = 1 ,append = select_list_nows)
    return select_list_nows

#选择储存器内容
def sl_list_select_stroer(arg):
    stroer_list = zx.textScrollList(select_list , query = 1 , si = 1 )
    zx.select(stroer_list)

#选择存储器
def sl_all_select_stroer(arg):
    stroer_list = zx.textScrollList(select_list , query = 1 , ai = 1 )
    zx.select(stroer_list)


#解包顶点索引
def unwrap_vertexlist(sl_lists):
    select_vertex_list = []
    for sl_list in sl_lists:
        index = sl_list[sl_list.find('['):]
        top_name = sl_list[:sl_list.find('[')]
        last_index = index[1:-1]
        if last_index.find(':') != -1:
            i = last_index.find(':')
            top = last_index[i+1:]
            down = last_index[:-i-1]
            if top.find(':')!= -1:
                c = int(top[1:])+1
            if down.find(':')!= -1:
                j = int(down[:-1])
            if top.find(':') == -1:
                c = int(top)+1
            if down.find(':')== -1:
                j = int(down)
            for i in range(j,c):
                wrap = top_name + '[' + str(i) + ']'
                select_vertex_list.append(wrap)
        else:
            select_vertex_list.append(sl_list)
    return select_vertex_list
#面到点，输出一个字典
def faceTovertex_unwrap(face_lists):
    vertex_dirct = {}
    n = 0
    for i in range(len(face_lists)):
        n = n + 1
        zx.select(face_lists[i])
        zx.ConvertSelectionToVertices()
        vertex_dirct[i] = unwrap_vertexlist(zx.ls(sl=1))
    print(vertex_dirct)
    return n , vertex_dirct 
#多边形重心计算
def focus_complate(vertex_input):

    #拿到起始顶点
    triangle_frist_X = vertex_input[:2][0]
    triangle_frist_Y = vertex_input[:2][1]

    #被链接顶点
    triangle_link = vertex_input[2:]
    XY_number = len(triangle_link)
    X_cuts = []
    Y_cuts = []

    #分离链接顶点
    n = -1
    j = 0
    for i in range(XY_number/2):
        n = n + 1
        j = j + 1
        U = i + n
        V = i + j  
        X_cuts.append(triangle_link[U])
        Y_cuts.append(triangle_link[V])

    #拿到每个三角形的重心
    triangle_focus_X = []
    triangle_focus_Y = []    
    for i in range(len(X_cuts) - 1):
        triangle_X_B = X_cuts[i]
        triangle_X_C = X_cuts[i + 1]

        triangle_Y_B = Y_cuts[i]
        triangle_Y_C = Y_cuts[i + 1]

        triangle_focus_X.append((triangle_frist_X + triangle_X_B + triangle_X_C) / 3.0)
        triangle_focus_Y.append((triangle_frist_Y + triangle_Y_B + triangle_Y_C) / 3.0)


    #计算平均重心
        centroid_X = triangle_focus_X[0]
        centroid_Y = triangle_focus_Y[0]
    
    for i in range(len(triangle_focus_X) - 1):
        centroid_X = (centroid_X + triangle_focus_X[i + 1]) / 2.0
        centroid_Y = (centroid_Y + triangle_focus_Y[i + 1]) / 2.0 
    
    return centroid_X , centroid_Y


#mesh_UV盒子中心计算
def mesh_boundbox_center(target):
    boundbox = zx.polyEvaluate(target , bc2=1)
    #(Xmin,Xmax),(Ymin,Ymax)
    boundbox_x = (boundbox[0][0] + boundbox[0][1])/2
    boundbox_y = (boundbox[1][0] + boundbox[1][1])/2
    return boundbox_x , boundbox_y


#UI本体
def build_xun_tool_UI():

    global yumaoyouguan
    global pilianggeigutou
    global dazushezhi
    global sidaiyaoyongdedongxi
    global piliangquanzhongdaorudaochu
    global yipifuyue
    global yipisuoyue
    global lock_tran
    global lock_rota
    global lock_scal
    global jnt_size_slider

    global zhijiedazu
    global pifuziyue
    global select_list
    global pisuofangyue
    global fol_grp_number
    global get_number
    global head_grp_number
    global last_grp_number
    global father_radio
    global chil_radio
    global both_radio
    global fol_num
    global zhongmao
    global pigeigu
    global zhijiedazu
    windows_name = '勋之工具箱'

    if zx.window(windows_name,query = True ,exists = True):
        zx.deleteUI(windows_name)

    kl = zx.window(windows_name )
    zx.showWindow()


    column_butonn = zx.columnLayout()
    changyongxiaogongneng =zx.frameLayout(label = '常用小功能(先父)' , w = 290)
    changyong = zx.flowLayout(cs=0 , h = 82)
    zx.setParent(changyong)
    zx.columnLayout()
    zx.button(label = '批简单父子' , 
            command = 'simple_parent(0)' , 
            h = 40)
    zx.button(label = '批带组父子', 
            command = 'simple_parent(1)'  , 
            h = 40)
    zx.setParent(changyong)
    zx.columnLayout()
    pifuziyue = zx.button(label = '对应批父子约' , 
                        command = 'Plural_parentconstraint(0)' , 
                        h = 40)
    yipifuyue = zx.button(label = '一对多父子约' , 
                        command = 'NoeTomore_parentconstraint(0)' ,
                        h = 40)
    zx.setParent(changyong)
    zx.columnLayout()
    pisuofangyue = zx.button(label = '对应批缩放约' ,
                        command = 'Plural_scaleconstraint(0)' , h = 40)
    yipisuoyue = zx.button(label = '一对多缩放约' ,
                        command = 'NoeTomore_scaletconstraint(0)' , h = 40)
    zx.setParent(changyong)
    zx.columnLayout()
    mo_radio_1 = zx.radioCollection()
    mo_radio = zx.radioButton('mo' ,
                            onc = '''zx.button(pifuziyue , edit = 1 , command = 'Plural_parentconstraint(1)' ) , zx.button(pisuofangyue , edit = 1 , command = 'Plural_scaleconstraint(1)') , zx.button(yipifuyue , edit = 1 , command = 'NoeTomore_parentconstraint(1)') , zx.button(yipisuoyue , edit = 1 , command = 'NoeTomore_scaletconstraint(1)') ''' , 
                            h = 20)
    no_mo_radio = zx.radioButton('no_mo' , 
                                onc = '''zx.button(pifuziyue , edit = 1 , command = 'Plural_parentconstraint(0)' ) , zx.button(pisuofangyue , edit = 1 , command = 'Plural_scaleconstraint(0)' ) , zx.button(yipifuyue , edit = 1 , command = 'NoeTomore_parentconstraint(0)') , zx.button(yipisuoyue , edit = 1 , command = 'NoeTomore_scaletconstraint(0)' )''' , 
                                h = 20 )

    zx.setParent(changyongxiaogongneng)
    asdasd = zx.flowLayout(cs=45 , h = 20)
    zx.radioCollection()
    zx.setParent(asdasd)
    zx.columnLayout()
    zx.radioButton('xyz',
                onc = '''zx.button(lock_tran , edit = 1 , command = 'all_lock_unlock_attr(0)' ) , zx.button(lock_rota , edit = 1 , command = 'all_lock_unlock_attr(1)' ) , zx.button(lock_scal , edit = 1 , command = 'all_lock_unlock_attr(2)')''',
                h = 20)
    zx.setParent(asdasd)
    zx.columnLayout()
    #奇数位置是rts通道，偶数位置对应的是xyz
    zx.radioButton('x',
                onc = '''zx.button(lock_tran , edit = 1 , command = 'lock_unlock_attr({},{})' ) , zx.button(lock_rota , edit = 1 , command = 'lock_unlock_attr({},{}) ') , zx.button(lock_scal , edit = 1 , command = 'lock_unlock_attr({},{})')'''.format(0,0,1,0,2,0),
                h = 20)
    zx.setParent(asdasd)
    zx.columnLayout()
    zx.radioButton('y',
                onc = '''zx.button(lock_tran , edit = 1 , command = 'lock_unlock_attr({},{})' ) , zx.button(lock_rota , edit = 1 , command = 'lock_unlock_attr({},{})' ) , zx.button(lock_scal , edit = 1 , command = 'lock_unlock_attr({},{})')'''.format(0,1,1,1,2,1),
                h = 20)
    zx.setParent(asdasd)
    zx.columnLayout()
    zx.radioButton('z',
                onc = '''zx.button(lock_tran , edit = 1 , command = 'lock_unlock_attr({},{})' ) , zx.button(lock_rota , edit = 1 , command = 'lock_unlock_attr({},{})' ) , zx.button(lock_scal , edit = 1 , command = 'lock_unlock_attr({},{})')'''.format(0,2,1,2,2,2),
                h = 20)
    zx.setParent(asdasd)




    zx.setParent(changyongxiaogongneng)
    channal_zero_box = zx.flowLayout(cs=0 , h = 80)
    zx.setParent(channal_zero_box)
    zx.columnLayout()
    zx.button(label = 'zero_tran' , 
            command = 'zero_Trans(1)' , 
            h = 40 , w = 80)
    lock_tran = zx.button(label = 'lock_tran' , 
                        command = '''all_lock_unlock_attr(0)''' ,
                        h = 40 , w = 80)
    zx.setParent(channal_zero_box)
    zx.columnLayout()
    zx.button(label = 'zero_rota' , 
            command = 'zero_Rota(1)' , 
            h = 40 , w = 80)
    lock_rota = zx.button(label = 'lock_rota' , 
                        command = '''all_lock_unlock_attr(1)''' , 
                        h = 40 , w = 80)
    zx.setParent(channal_zero_box)
    zx.columnLayout()
    zx.button(label = 'zero_scal' , 
            command = 'zero_Scale(1)' , 
            h = 40 , w = 80)
    lock_scal = zx.button(label = 'lock_scal' , 
                        command = '''all_lock_unlock_attr(2)''' , 
                        h = 40 , w = 80)




    zx.setParent(column_butonn)
    column_fol = zx.columnLayout()
    yumaoyouguan = zx.frameLayout(label = '与毛有关(Follice)' , la = 'top' , w = 290 , h =70 , cll = 1 , cl = 0 , cc = 'zx.frameLayout(yumaoyouguan , edit = 1 , h = 20)' , ec = 'zx.frameLayout(yumaoyouguan , edit = 1 , h = 70)')
    zx.setParent(yumaoyouguan)
    fol_int = zx.flowLayout(cs=1 , h = 100 , w = 290)
    zx.frameLayout(label = '毛内组：' , w = 60)
    fol_grp_number = zx.intField(min = 0 , max = 40 , v = 0 , h = 20)
    zx.setParent(fol_int)
    zx.button(label = '建立毛囊' , command = 'create_fol_v_e_f(1)' ,h = 40)
    zx.button(label = '可控化' , command = 'use_controlled_fol(1)' , h = 40)
    zx.button(label = '毛囊吸附' , command = 'fol_rematch(1)' , h = 40)
    zx.button(label = '报数' , command = 'number_taller(1)', h = 40)
    zx.setParent(fol_int)
    number_int = zx.flowLayout(cs=1 , h = 100 , w = 290)
    zx.frameLayout(label = '报数：' , w = 40)
    get_number = zx.intField(min = 0 , v = 0 , h = 20)


    zx.setParent(column_butonn)
    column_jnt = zx.columnLayout()
    pilianggeigutou = zx.frameLayout(label = '批量给骨头（顺序很重要哥么）' , la = 'top' , w = 290 , h =120 , cll = 1 , cl = 0 , cc = 'zx.frameLayout(pilianggeigutou , edit = 1 , h = 20)' , ec = 'zx.frameLayout(pilianggeigutou , edit = 1 , h = 120)')

    zx.setParent(pilianggeigutou)
    jnt_int = zx.flowLayout(cs=1 , h = 60 , w = 290)

    zx.frameLayout(label = '要组?' , w = 40)
    zu_radio_2 = zx.radioCollection()
    have_grp = zx.radioButton('yep' , onc = '''zx.button(pigeigu,edit=1,command = 'groupTojoint(0)')''' , h = 20)
    no_grp = zx.radioButton('no' , sl=1 , onc = '''zx.button(pigeigu,edit=1,command = 'Plural_joint(1)')''', h = 20)

    zx.setParent(jnt_int)
    pigeigu = zx.button(label = '批给骨' , command = 'Plural_joint(1)' , ann = '按所选批量新建骨头' , h = 60)
    zx.button(label = '批偏骨' , command = 'zx_matchtrans(1)', h = 60)
    zx.button(label = 'free_S_R',command = 'freeze_trans(1)' , h = 60)
    zx.iconTextButton(label = '定向骨头' , command = '''mel.eval('joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;')''' , dcc = '''zx.OrientJointOptions()''' , image1 = '''orientJoint.png''' , style = 'iconAndTextVertical'   , h = 60 )
    zx.iconTextButton(label = '曲线ik' , command = '''mel.eval('IKSplineHandleTool;')''' , dcc = '''mel.eval('IKSplineHandleToolOptions;')''' , image1 = '''kinSplineHandle.png''' , style = 'iconAndTextVertical'   , h = 60 )

    zx.setParent(pilianggeigutou)
    zx.columnLayout()
    jnt_size_slider = zx.floatSlider(min = 0 , max = 1.5 , step = 1 , 
                w = 270 ,
                cc = 'jnt_size_change(1)')
    zx.button(label = '获得选择对应蒙皮骨骼',command = 'get_skincluster_jnt(1)' , h = 20 , w= 290)



    zx.setParent(column_butonn)
    column_grp = zx.columnLayout()
    dazushezhi = zx.frameLayout(label = '打组设置（all_set）' , la = 'top' , w = 290 , h =45 , cll = 1 , cl = 0 , cc = 'zx.frameLayout(dazushezhi , edit = 1 , h = 20)' , ec = 'zx.frameLayout(dazushezhi , edit = 1 , h = 45)')
    zx.flowLayout(cs=1 , h = 40 , w = 290)
    zhijiedazu = zx.button(label = '直接打组' , command = 'Plural_group(1)' , h = 20)
    head_grp_number = zx.intField(min = 0 , max = 40 , v = 0 , h = 20)
    zu_radio_3 = zx.radioCollection()
    father_radio = zx.radioButton('father' , onc = '''zx.button(zhijiedazu , edit = 1 , command = 'Plural_group(0)' ) ''' , h = 20)
    last_grp_number = zx.intField(min = 0 , max = 40 , v = 0 , h = 20)
    chil_radio = zx.radioButton('chil' , onc = '''zx.button(zhijiedazu , edit = 1 , command = 'Plural_group(1)' ) ''' , h = 20)
    both_radio = zx.radioButton('both' ,  onc = '''zx.button(zhijiedazu , edit = 1 , command = 'Plural_group(2)' ) ''' , h = 20)
    


    zx.setParent(column_butonn)
    column_ribbon = zx.columnLayout()
    sidaiyaoyongdedongxi = zx.frameLayout(label = '丝带本体' , la = 'top' , w = 290 , h =175 , cll = 1 , cl = 0 , cc = 'zx.frameLayout(sidaiyaoyongdedongxi , edit = 1 , h = 20)' , ec = 'zx.frameLayout(sidaiyaoyongdedongxi , edit = 1 , h = 175)')
    zx.flowLayout(cs=1 , h = 40 , w = 270)
    zx.iconTextButton(label = '绘制曲线' , command = 'zx.EPCurveTool()' , image1 = 'curveEP.png' , style = 'iconAndTextVertical'   , h = 60 )
    zx.iconTextButton(label = '重建曲线' , command = 'zx.RebuildCurve()' , dcc = 'zx.RebuildCurveOptions()', image1 = 'rebuildCurve.png' , style = 'iconAndTextVertical'   , h = 60 )
    zx.iconTextButton(label = '放样' , command = 'zx.Loft()', dcc = 'zx.LoftOptions()', image1 = 'skin.png' , style = 'iconAndTextVertical'   , h = 60 )
    zx.iconTextButton(label = '翻转曲面' , command = 'zx.reverseSurface()' , dcc = 'zx.ReverseSurfaceDirectionOptions()' , image1 = 'reverseSurface.png' , style = 'iconAndTextVertical'   , h = 60 )
    zx.iconTextButton(label = '重建曲面' , command = 'zx.RebuildSurfaces()' , dcc = 'zx.RebuildSurfacesOptions()', image1 = 'rebuildSurface.png' , style = 'iconAndTextVertical'   , h = 60 )

    zx.setParent(sidaiyaoyongdedongxi)
    fol_ins = zx.flowLayout(cs = 5)
    zhongmao = zx.iconTextButton(label = '种毛' ,command = 'flocking_fol(0)', image1 = 'hairCreate.png' , style = 'iconAndTextVertical'   , h = 60 )
    zx.setParent(fol_ins)
    zx.columnLayout()
    fol_num = zx.intField(min = 0 , max = 40 , v = 0 , h = 20 , w = 40)
    zu_radio_4 = zx.radioCollection()
    fol_U = zx.radioButton('U' , onc = '''zx.iconTextButton(zhongmao , edit = 1 , command = 'flocking_fol(0)')''' , h = 20 , w = 40)
    fol_V = zx.radioButton('V' , onc = '''zx.iconTextButton(zhongmao , edit = 1 , command = 'flocking_fol(1)')''' , h = 20 , w = 40)
    zx.setParent(fol_ins)
    zx.button(label = 'check' , command = 'check(1)' , h = 60 , w = 80)
    zx.setParent(fol_ins)
    zx.button(label = '逆矩阵' , command = 'faker_ui(1)' , h = 60 , w = 80)

    #一、设置菜单名称
    zx.setParent(column_butonn)
    piliangquanzhongdaorudaochu = zx.frameLayout(label = '批量权重导入导出' , h = 100 , cll = 1 , cl = 0 , cc = 'zx.frameLayout(piliangquanzhongdaorudaochu , edit = 1 , h = 20)' , ec = 'zx.frameLayout(piliangquanzhongdaorudaochu , edit = 1 , h = 100)')
    zx.gridLayout(numberOfColumns = 1 , cellWidth = 290)
    zx.textField('Fk0')
    zx.setParent(piliangquanzhongdaorudaochu)
    zx.flowLayout(cs=2 , h = 40 , w = 270)
    zx.button(label = '导入',command = 'Plural_input_skin(1)' , w = 100 , h = 40)
    zx.button(label = '导出',command = 'Plural_output_skin(1)' , w = 100, h = 40)

    zx.setParent(column_butonn)
    column_store = zx.columnLayout()
    zx.frameLayout(label = '选择信息储存' , cll = 1 , cl = 0 , w = 290)
    select_list = zx.textScrollList(ams = 1 ,  h = 100)
    zx.flowLayout()
    zx.button(label = '存储选择' , command = 'select_stroer(1)' ,  h = 50 , w = 170)  
    zx.button(label = '选择部分' , command = 'sl_list_select_stroer(1)' ,  h = 50 , w = 60)  
    zx.button(label = '选择全部' , command = 'sl_all_select_stroer(1)' ,  h = 50 , w = 60)  

    
#常用小功能

#简单父子
def simple_parent(switch_number):
    #用1和0来切换，有组或者无组的
    q = zx.ls(sl=1)
    for i in range(len(q)-1):        
        if switch_number == 0:
            
            zx.parent(q[i+1] , q[i])
        if switch_number == 1:    
            list_chil = zx.listRelatives(q[i],ad=1)[0]
            zx.parent(q[i+1],list_chil)

#批量约束
def Plural_parentconstraint(offset_mo):
    #父级
    if zx.textScrollList(select_list , query = 1 , ai = 1) != 0:
        parent_list = zx.textScrollList(select_list , query = 1 , ai = 1)
        child_list = zx.ls(sl = 1)
        for i in range(len(child_list)): 
            j = zx.parentConstraint(parent_list[i] , child_list[i] , mo = offset_mo )
    
    return j

def NoeTomore_parentconstraint(offset_mo):
    if zx.textScrollList(select_list , query = 1 , ai = 1) != 0:
        target_a = zx.textScrollList(select_list , query = 1 , ai = 1)[0]
        for i in zx.ls(sl=1):
            j = zx.parentConstraint(target_a,i,mo=offset_mo)
    return j

def Plural_scaleconstraint(offset_mo):
    #缩放
    if zx.textScrollList(select_list , query = 1 , ai = 1) != 0:
        parent_list = zx.textScrollList(select_list , query = 1 , ai = 1)
        child_list = zx.ls(sl = 1)
        for i in range(len(child_list)): 
            j = zx.scaleConstraint(parent_list[i] , child_list[i] , mo = offset_mo )
    return j

def NoeTomore_scaletconstraint(offset_mo):
    if zx.textScrollList(select_list , query = 1 , ai = 1) != 0:
        target_a = zx.textScrollList(select_list , query = 1 , ai = 1)[0]
        for i in zx.ls(sl=1):
            j = zx.scaleConstraint(target_a,i,mo=offset_mo)
    return j

#清空数值
def zero_Trans(arg):
    tar_a = zx.ls(sl=1,type='transform')
    for i in tar_a:
        if zx.getAttr('%s.tx'%i,l=1) == False:
            zx.setAttr('%s.tx'%i,0)
    for i in tar_a:
        if zx.getAttr('%s.ty'%i,l=1) == False:
            zx.setAttr('%s.ty'%i,0)
    for i in tar_a:
        if zx.getAttr('%s.tz'%i,l=1) == False:
            zx.setAttr('%s.tz'%i,0)

def zero_Rota(arg):
    tar_a = zx.ls(sl=1,type='transform')
    for i in tar_a:
        if zx.getAttr('%s.ry'%i,l=1) == False:
            zx.setAttr('%s.ry'%i,0)
    for i in tar_a:
        if zx.getAttr('%s.rx'%i,l=1) == False:
            zx.setAttr('%s.rx'%i,0)
    for i in tar_a:
        if zx.getAttr('%s.rz'%i,l=1) == False:
            zx.setAttr('%s.rz'%i,0)

def zero_Scale(arg):
    tar_a = zx.ls(sl=1,type='transform')
    for i in tar_a:
        if zx.getAttr('%s.sz'%i,l=1) == False:
            zx.setAttr('%s.sz'%i,1)
    for i in tar_a:
        if zx.getAttr('%s.sy'%i,l=1) == False:
            zx.setAttr('%s.sy'%i,1)
    for i in tar_a:
        if zx.getAttr('%s.sx'%i,l=1) == False:
            zx.setAttr('%s.sx'%i,1)

def lock_unlock_attr(t_num,x_num):
    trans = ['t' , 'r' , 's'] 
    asiex = ['x' , 'y' , 'z']
    check = {}
    for k in zx.ls(sl=1):
        check[k] = zx.getAttr('{}.{}{}'.format(k , trans[t_num] , asiex[x_num]) , l=1)
        if zx.getAttr('{}.{}{}'.format(k , trans[t_num] , asiex[x_num]) , l=1) == True:
            zx.setAttr('{}.{}{}'.format(k , trans[t_num] , asiex[x_num]) , l = 0)
        else: 
            zx.setAttr('{}.{}{}'.format(k , trans[t_num] , asiex[x_num]) , l = 1)        
    return check

def all_lock_unlock_attr(t_num):
    trans = ['t' , 'r' , 's'] 
    for k in range(3):
        lock_unlock_attr(t_num,k)




#与毛有关
def get_pointTo_UV(sl_lists):

    UVValues = []
    for sl_list in sl_lists:
        zx.select(sl_list)
        zx.ConvertSelectionToUVs()
        sl_to_UV = zx.polyEditUV(query=True)
          # 这里输出一个顶点
        for i in range(2):
            UVValues.append(sl_to_UV[i])
          
    return UVValues

def One_follcile(Tar_FolU_FolV):

    target_a = Tar_FolU_FolV[0]

    
    fol_numberToU = Tar_FolU_FolV[1]
    fol_numberToV = Tar_FolU_FolV[2]
            
    insurface = zx.listRelatives(target_a,c=1)[0]
    fol_shape = zx.createNode('follicle' , name = double_nameadd('zexxun_folicle_shape'))
    fol_trans = zx.listRelatives(fol_shape,p=1)[0]
    zx.connectAttr('%s.outTranslate' % fol_shape , '%s.translate' % fol_trans,f=1)
    zx.connectAttr('%s.outRotate' % fol_shape , '%s.rotate' % fol_trans,f=1)
    zx.setAttr('%s.parameterU' % fol_shape , fol_numberToU)
    zx.setAttr('%s.parameterV' % fol_shape , fol_numberToV)

    type_nurbs_surface_check = zx.listRelatives(target_a , type = 'nurbsSurface')
    type_mesh_check = zx.listRelatives(target_a , type = 'mesh')
    
    if type_nurbs_surface_check != None:
        zx.connectAttr('%s.local' % insurface , '%s.inputSurface' % fol_shape,f=1)
        zx.connectAttr('%s.worldMatrix' % insurface , '%s.inputWorldMatrix' % fol_shape,f=1)
    if type_mesh_check != None:
        zx.connectAttr('%s.outMesh' % insurface , '%s.inputMesh' % fol_shape,f=1)
        zx.connectAttr('%s.worldMatrix' % insurface , '%s.inputWorldMatrix' % fol_shape,f=1)
    return fol_trans

#毛囊
def create_fol_vertex(vertex):  
    
    fol_list = []
    sl_lists = unwrap_vertexlist(vertex)
    UVValues = get_pointTo_UV(sl_lists)

    UV_number = len(UVValues)
    
    n = -1
    j = 0
    for i in range(int(UV_number/2)):
        input_one_follcile = []
        create_target = zx.textScrollList(select_list , query = 1 , ai = 1)
        input_one_follcile.append(create_target)

        n = n + 1
        j = j + 1
        U = i + n
        V = i + j  

        input_one_follcile.append(UVValues[U])
        input_one_follcile.append(UVValues[V])
        fol_trans = One_follcile(input_one_follcile)
        fol_list.append(fol_trans)

    return fol_list

def create_fol_edge(vertexs):
    fol_list = []
    for vertex in vertexs:
        zx.select(vertex)
        zx.ConvertSelectionToVertices()
        zx.ConvertSelectionToUVs()
        boundingboxx2d_UV = zx.polyEvaluate(bc2=1)
        print(boundingboxx2d_UV)
        focus_U = ((boundingboxx2d_UV[0][0] + boundingboxx2d_UV[0][1])/2 )+ 1e-5
        focus_V = ((boundingboxx2d_UV[1][0] + boundingboxx2d_UV[1][1])/2) + 1e-5
        input_one_follcile = []
        create_target = zx.textScrollList(select_list , query = 1 , ai = 1)
        input_one_follcile.append(create_target)
        input_one_follcile.append(focus_U )
        input_one_follcile.append(focus_V)
        fol_trans = One_follcile(input_one_follcile)
        fol_list.append(fol_trans)

    return fol_list

def create_fol_face(face_lists):  
    
    fol_list = []

    #分组输入拿最终重心uv坐标
    for i in range(len(face_lists)):     
        zx.select(face_lists[i])
        zx.ConvertSelectionToUVs()
        boundingboxx2d_UV = zx.polyEvaluate(bc2=1)
        focus_U = ((boundingboxx2d_UV[0][0] + boundingboxx2d_UV[0][1])/2 )+ 1e-5
        focus_V = ((boundingboxx2d_UV[1][0] + boundingboxx2d_UV[1][1])/2) + 1e-5

        input_one_follcile = []
        create_target = zx.textScrollList(select_list , query = 1 , ai = 1)
        input_one_follcile.append(create_target)

        input_one_follcile.append(focus_U)
        input_one_follcile.append(focus_V)
        fol_trans = One_follcile(input_one_follcile)
        fol_list.append(fol_trans)
    
    
    return fol_list

def create_fol_v_e_f(arg):

    select_list = unwrap_vertexlist(zx.ls(sl=1))
    print(select_list)
    k = zx.intField(fol_grp_number , query = 1 ,v = 1)
    index = select_list[0].find('.')

    if select_list[0][index+1:index+2] == 'v':
        print('vertex')

        fol_lists = (create_fol_vertex(select_list))
        for fol_list in fol_lists:
            for i in range(k):
                zx.select(deselect=1)
                g = zx.group(em=1)

                zx.parent(g,fol_list)
                zx.select(deselect=1)
    if select_list[0][index+1:index+2] == 'e':
        print('edge')
         
        fol_lists = (create_fol_edge(select_list))
        for fol_list in fol_lists:
            for i in range(k):
                zx.select(deselect=1)
                g = zx.group(em=1)

                zx.parent(g,fol_list)
                zx.select(deselect=1)

    if select_list[0][index+1:index+2] == 'f':
        print('face')

        fol_lists = create_fol_face(select_list)
        for fol_list in fol_lists:
            for i in range(k):
                zx.select(deselect=1)
                g = zx.group(em=1)

                zx.parent(g,fol_list)
                zx.select(deselect=1)
    print(fol_lists)            
    
    return fol_lists

#可控化
def controlled_fol(fol_listk):

    #输入一个元组

    target_a = fol_listk[0][0]

    fol_lists = fol_listk[1]

    close_point_Node = []

    loc_lists = []

    for fol_list in fol_lists:
        print(fol_list)
        fol_shape = zx.listRelatives(fol_list , c = 1)[0]

        loc_name = zx.spaceLocator(name = '%s_loc'%fol_list)[0]
        loc_lists.append(loc_name)

        zx.select(loc_name)
        zx.select(fol_list,add=1)
        zx.matchTransform()

        type_nurbs_surface_check = zx.listRelatives(target_a , type = 'nurbsSurface')
        type_mesh_check = zx.listRelatives(target_a , type = 'mesh')

        if type_nurbs_surface_check != None:
            close_sur = zx.createNode('closestPointOnSurface')
            zx.connectAttr('%s.worldSpace'%target_a , '%s.inputSurface'%close_sur,f=1)
            zx.connectAttr('%s.translate'%loc_name , '%s.inPosition'%close_sur,f=1)
            zx.connectAttr('%s.result.parameterU'%close_sur , '%s.parameterU'%fol_shape,f=1)
            zx.connectAttr('%s.result.parameterV'%close_sur , '%s.parameterV'%fol_shape,f=1)

            close_point_Node.append(close_sur)   


        if type_mesh_check != None:
            close_mesh = zx.createNode('closestPointOnMesh')
            zx.connectAttr('%s.outMesh'%target_a , '%s.inMesh'%close_mesh,f=1)
            zx.connectAttr('%s.translate'%loc_name , '%s.inPosition'%close_mesh,f=1)
            zx.connectAttr('%s.result.parameterU'%close_mesh , '%s.parameterU'%fol_shape,f=1)
            zx.connectAttr('%s.result.parameterV'%close_mesh , '%s.parameterV'%fol_shape,f=1)

            close_point_Node.append(close_mesh)
    print(close_point_Node , loc_lists)        
    return close_point_Node , loc_lists

def use_controlled_fol(arg):
    input_controlled_fol = (zx.textScrollList(select_list , query = 1 , ai = 1) , zx.ls(sl=1))
    controlled_fol(input_controlled_fol)

#毛囊吸附
def fol_rematch(arg):

    fol_lists = zx.ls(sl=1)
    match_target = zx.textScrollList(select_list , query = 1 , ai = 1)

    if len(match_target) != len(zx.ls(sl=1)):
        print('错错错错错错错错错错错错错错错错错错错错错错错错错错错错错错错错错错错:你妈的这数量不一样啊？你还想匹配？做梦呢？是不是又是不爱看控制台报错了？？？？？我这个不红不看是吧？？？？？')

    else:
        target_a = zx.listConnections('%s.inputMesh'%fol_lists[0])
        if target_a == None:
            target_a = zx.listConnections('%s.inputSurface'%fol_lists[0])
        
        k = (target_a , fol_lists)
        print(k)
        do_def =  controlled_fol(k)
        loc_lists = do_def[1]
    
        for i in range(len(loc_lists)):
            zx.select(loc_lists[i])
            zx.select(match_target[i] , add=1)
            zx.matchTransform()
            zx.delete(loc_lists[i])
    
    print('匹配完了兄弟姐么')

def number_taller(arg):
    zx.intField(get_number , edit = 1, v = len(zx.ls(sl=1)))



#打组类
def Plural_group(L):
    #根据123选择怎么打组
    targets = zx.ls(sl=1)
    ui = zx.listRelatives(targets , p = 1)
    if ui != None:
        orignal_fas = zx.listRelatives(targets , p = 1)
    father_list = []
    child_list = []

    #0只打father
    if L == 0:
        f = 1
        c = 0
    #1只打儿子
    if L == 1:
        f = 0
        c = 1
    #2全打一遍
    if L == 2:
        f = 1
        c = 1
    n = -1
    for target in targets:
        n += 1
        p = []
        z = []
        num_father_group = zx.intField(head_grp_number , query=1 , v = 1)
        num_child_group = zx.intField(last_grp_number , query=1 , v = 1)
        if f == 1:
            if num_father_group != 0:
                for i in range(num_father_group) :
                    zx.select(deselect=1)
                    gp_head = zx.group(em=1)
                    zx.select(gp_head)
                    zx.select(target,add=1)
                    zx.matchTransform()
                    father_list.append(gp_head)
                    p.append(gp_head)
                if len(p) > 1:
                    for i in range(len(p)-1):
                        zx.parent(p[i] , p[i+1])
                zx.parent(target , p[0])
                if ui != None:
                    if len(p) > 1:
                        zx.parent(p[i+1] , orignal_fas[n])
                    if len(p) <= 1:
                        zx.parent(p[0] , orignal_fas[n])
        if c == 1:
            if num_child_group != 0:
                for i in range(num_child_group) :
                    zx.select(deselect=1)
                    gp_child = zx.group(em=1)
                    zx.select(gp_child)
                    zx.select(target,add=1)
                    zx.matchTransform()
                    z.append(gp_child)
                    child_list.append(gp_child)
                for i in range(len(z)-1):
                    zx.parent(z[i] , z[i+1])
                zx.parent(gp_child , target)


    return father_list , child_list

#骨头类
def Plural_joint(arg):
    target_a = zx.ls(sl = 1)
    jointlist = []
    for target in target_a:
        zx.select(deselect=1)
        target_position = zx.xform(target , query = 1 , piv = 1 , ws = 1 )[3:]
        joint_name = zx.joint(p = target_position)
        zx.select(joint_name)
        zx.select(target,add=1)
        zx.matchTransform()
        jointlist.append(joint_name)
    return jointlist

def freeze_trans(arg):
    sl_list = zx.ls(sl=1)
    mel.eval('makeIdentity -apply true -t 0 -r 1 -s 1 -n 0 -pn 1;')
    c = zx.spaceLocator()
    zx.select(c)
    mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
    zx.delete(c)
    zx.select(sl_list)

def zx_matchtrans(arg):
    target_a = zx.textScrollList(select_list , query = 1 , ai = 1)
    target_b = zx.ls(sl = 1)
    for i in range(len(target_a)):
        zx.select(target_b[i])
        zx.select(target_a[i],add=1)
        zx.matchTransform()

def test(arg):
    fat_radio = zx.radioButton(father_radio , query = 1 , sl = 1)
    print(fat_radio)

def groupTojoint(L):
    joints = Plural_joint(1)
    for jointk in joints:
        zx.select(jointk)
        Plural_group(L)

def jnt_size_change(arg):
    
    zx.jointDisplayScale(zx.floatSlider(jnt_size_slider , query = 1 , value = 1))



#丝带种毛部分
def flocking_fol(L):
    target_a = zx.ls(sl=1)
    fol_number = zx.intField(fol_num , query=1,v=1)
    fol_trans = []
    fol_distance = 1.000/(fol_number - 1.000)
    n = -fol_distance
    for i in range(fol_number):
        input_One_follcile = []
        
        input_One_follcile.append(target_a)
        n += fol_distance
        if L == 0:
            U = n
            V = 0.5
        if L == 1:
            V = n
            U = 0.5
        input_One_follcile.append(U)
        input_One_follcile.append(V)

        fol_trans.append(One_follcile(input_One_follcile))

    return fol_trans


#文件检查
def check(arg):
    #列出所有的namespace
    zx.namespace(setNamespace=':')
    #递归掉Ui和shared
    all_namespaces = [x for x in zx.namespaceInfo(listOnlyNamespaces=True, recurse=True) if x != "UI" and x != "shared"]

    if all_namespaces:
            # Sort by hierarchy, deepest first.这段不懂
        all_namespaces.sort(key=len, reverse=True)
        for namespace in all_namespaces:
            # 检测名称是否存在后执行删除
            if zx.namespace(exists=namespace) is True:
                zx.namespace(removeNamespace=namespace, mergeNamespaceWithRoot=True)


    #删除所有层
    #递归
    layer = [ x for x in zx.ls(type="displayLayer" ) if x != 'defaultLayer' and  x != 'jointLayer']
    #执行删除
    if layer != []:
        zx.delete(layer)

    #删除未知节点
    for i in zx.ls(type = 'unknown'):
        if i in zx.ls(type = 'unknown'):
            zx.delete(i)

    #删除未使用着色
    mel.eval(' MLdeleteUnused;')

    #隐藏DeformationSystem
    for i in zx.ls(type="transform" ):  
        q = i.find('DeformationSystem')
        if q != -1 :
            zx.hide(i)

    #线框显示同时隐藏joint
    zx.modelEditor('modelPanel4',e=True,joints = False,swf = True,displayAppearance='wireframe')

    #删除未知插件
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    c = zx.unknownPlugin(query=1,list=1)
    if c != None:
        for i in c:
            zx.unknownPlugin(i,remove=1)
        
        
    for modelPanel in zx.getPanel (type = "modelPanel" ):
        if zx.modelEditor ( modelPanel, q = 1,ec = 1 ) == "CgAbBlastPanelOptChangeCallback":
            zx.modelEditor ( modelPanel, e = 1,ec = "" )

    #关闭UI自动保存
    zx.file(uc=0)

    #删除
    for i in zx.ls(type = 'script'):
        if i == 'uiConfigurationScriptNode':
            zx.delete('uiConfigurationScriptNode')

    #清除关键帧
    zx.select(deselect=1)
    keyframe_list = []
    for i in zx.ls(type = 'animCurveTA'):
        keyframe_list.append(i)
    for i in zx.ls(type = 'animCurveTL'):
        keyframe_list.append(i)
    for i in zx.ls(type = 'animCurveTU'):
        keyframe_list.append(i)    
    if len(keyframe_list) != 0:
        zx.delete(keyframe_list)

    #maya杀毒，你必须自己安装
    if zx.pluginInfo('MayaScanner.py' , query=1 , l=1) == False:
        zx.loadPlugin('MayaScanner.py')
        zx.pluginInfo('MayaScanner.py' , e=1 , autoload=1)
    if zx.pluginInfo('MayaScannerCB.py' , query=1 , l=1) == False:
        zx.loadPlugin('MayaScannerCB.py')
        zx.pluginInfo('MayaScannerCB.py' , e=1 , autoload=1)


#批量导入导出权重
def Plural_output_skin(*arg):
    outputd = zx.textField('Fk0',query = True ,text = True)
    outputd.replace("\r" , "/r")
    print(outputd)
    objlsits = zx.ls(sl=True)
    for i in range(0,len(zx.ls(sl = True))):
        for objlsit in objlsits:
            shapes = zx.listRelatives(objlsit, shapes=True)#这里获得了形状节点
            history = zx.listHistory(shapes, groupLevels=True, pruneDagObjects=True)#这里获得了history
            skins = zx.ls(history, type='skinCluster')#通过history获得了蒙皮的数据
            for skin in skins:
                print(skins)

                zx.deformerWeights('%s.xml'%objlsit,export =True ,deformer =skin,path = format(outputd) )


def Plural_input_skin(*arg):
    outputd = zx.textField('Fk0',query = True ,text = True)
    objlsits = zx.ls(sl=True)
    outputd.replace("\r" , "/r")
    for i in range(0,len(zx.ls(sl = True))):
        for objlsit in objlsits:
            shapes = zx.listRelatives(objlsit, shapes=True)#这里获得了形状节点
            history = zx.listHistory(shapes, groupLevels=True, pruneDagObjects=True)#这里获得了history
            skins = zx.ls(history, type='skinCluster')#通过history获得了蒙皮的数据
            for skin in skins:
                print(skins)
                zx.deformerWeights('%s.xml'%objlsit,im =True ,method ="index" ,deformer = skin,path = format(outputd))
                zx.skinCluster(skin,e=True,forceNormalizeWeights =True)






####################################逆矩阵##############################
####################################################毛囊生成器######################################################


def creatfolliceleinvertex(mesh):



    global lgrps




    ####################顶点生成毛囊################
    # 拿到UV坐标
    selectvertexs = mc.ls(sl=True, sn=1)
    mc.ConvertSelectionToUVs()
    UVValues = mc.polyEditUV(query=True)  # 这里输出一个顶点
    first = len(UVValues)
    n = -1

    # 这里做检测后建立总组
    list = [str(r) for r in mc.ls(type='transform')]
    n = 0
    grp_name = 'Follice_grp_%s' % mesh

    while grp_name in list:
        n = n + 1
        grp_name = 'Follice_grp_%s' % mesh + '_%s' % n
    mc.group(name=grp_name, em=1)


    check = mc.ls(type='follicle')
    q = len(check)
    # 双数切片
    for i in range(int(first/2)):
        q = q+1
        z = '%s' % i
        next = first-1
        first = next-1

        U = UVValues[first]
        V = UVValues[next]

        fol_nodename = '%s_attach' % mesh + '_%s' % z
        fol_transname = '%s_trans' % mesh + '_%s' % z

        if fol_nodename in check:
            z = '_%s' % q
            fol_nodename = '%s_attach' % mesh + '_%s' % z
            fol_transname = '%s_trans' % mesh + '_%s' % z
        else:
            k=0

        lgrps.append(fol_transname)

        fol = mc.createNode("follicle", name=fol_nodename)
        fol_trans = mc.listRelatives(p=True)[0]
        mc.rename(fol_trans, fol_transname)

        mc.connectAttr("%s.outMesh" % mesh, "%s.inputMesh" %
                       fol_nodename, force=True)
        mc.connectAttr(
            "%s.worldMatrix[0]" % mesh, "%s.inputWorldMatrix" % fol_nodename, force=True)
        mc.connectAttr("%s.outTranslate" % fol_nodename,
                       "%s.translate" % fol_transname, force=True)
        mc.connectAttr("%s.outRotate" % fol_nodename,
                       "%s.rotate" % fol_transname, force=True)
        mc.setAttr("%s.parameterU" % fol_nodename, U)
        mc.setAttr("%s.parameterV" % fol_nodename, V)
        mc.setAttr("%s.translate" % fol_transname, lock=True)
        mc.setAttr("%s.rotate" % fol_transname, lock=True)

    for lgrp in lgrps:
        mc.parent(lgrp, grp_name)
    return lgrps

#############################################获得曲线形状###########################
# 这里输入给定的shape

#获得控制器形状
def getshape(crvShapes):



    global crvShapeDict



    # 使用曲线属性节点
    curve_info_name = 'KB1'
    mc.createNode('curveInfo', name=curve_info_name)
    mc.connectAttr('%s.worldSpace' % crvShapes,
                   '%s.inputCurve' % curve_info_name)

    # 获得了Knots
    crvShapeDict["knots"] = mc.getAttr('%s.knots[*]' % curve_info_name)

    # 获得points
    crvShapeDict["points"] = mc.getAttr(
        '%s.controlPoints[*]' % curve_info_name)
    mc.delete(curve_info_name)

    # 获得form
    crvShapeDict["form"] = mc.getAttr(crvShapes + ".form")

    # 获得degree
    crvShapeDict["degree"] = mc.getAttr(crvShapes + ".degree")

    # 获得overideColor
    crvShapeDict["overrideColor"] = mc.getAttr(crvShapes + ".overrideColor")
    return crvShapeDict


#创建根骨
def creatroot(*arg):
    # 创建根骨
    mesh = mc.textField('mesh',query = True ,text = True)
    roobname = 'Faker_root' + '_%s' % mesh
    mc.group(em=1, name='Faker_DEF' + '_%s' % mesh )
    mc.joint(p=(0, 0, 0), name=roobname)
    return roobname


#根据已有的毛生成控制器
def creatfolandctrl(*arg):
    ##############################创建毛囊创建控制器##########################

                    ###################全局变量###################

    global PDJDict

    global lgrps ################毛囊_列表

    global crvShapeDict###控制器形状_字典




    mesh = mc.textField('mesh',query = True ,text = True) ##########原始网格

    crvShapes = mc.textField('crvShapes',query = True ,text = True)#这里给入shape

    #调用函数执行



    getshape( crvShapes )#拿到控制器形状，必须是curve


    #####################################################执行段落############################################################

    # 根据字典创建形状
    list = [str(r) for r in mc.ls(type='transform')]

    n = 0
    mo_grp = 'Fol_motion'

    # 这里做检测后建立总组
    while mo_grp in list:
        n = n + 1
        mo_grp = 'Fol_motion%s' % n


    mc.group(name=mo_grp, em=1)

    J_list = []
    D_list = []
    P_list = []

    q = len(lgrps)
    # 创建根据拾取的形状创建控制器
    for lgrp in range(q):

        # 检测名称
        ctrl_name = 'fol_ctrl_%s' % mesh + '_%s' % lgrp
        while ctrl_name in list:
            q = q + 1
            ctrl_name_add = '_%s' % q
            ctrl_name = 'fol_ctrl_%s' % mesh + ctrl_name_add

        # 创建形状
        mc.curve(p=crvShapeDict["points"], k = crvShapeDict["knots"],
                d=crvShapeDict["degree"], per = bool(crvShapeDict["form"]), name = ctrl_name)

        mc.select(ctrl_name)

        mogrp_Parent_name = 'parent_' + ctrl_name
        mogrp_Dive_name = 'Dive' + ctrl_name

        mc.group(name = mogrp_Dive_name)
        mc.group(name = mogrp_Parent_name)

        mc.parent(mogrp_Parent_name , mo_grp)

        # 创建骨骼
        joint_name = ctrl_name.replace('ctrl_', 'joint_')
        mc.joint(p = (0, 0, 0), name = joint_name)
        joint_grp_name = ctrl_name.replace('ctrl_', 'joint_offset_')
        mc.group(name = joint_grp_name )
        mc.parent(joint_grp_name, ctrl_name)

        J_list.append(joint_name)
        D_list.append(mogrp_Dive_name)
        P_list.append(mogrp_Parent_name)

    # 存列表
    PDJDict['P_list'] = P_list
    PDJDict['D_list'] = D_list
    PDJDict['J_list'] = J_list

    q =  PDJDict['P_list']

    for i in range(len(lgrps)):
        # 约束给毛囊
        mc.parentConstraint(lgrps[i], q[i])
    return PDJDict


#第一次蒙皮
def firstsecCluster(*arg):


    global PDJDict
    PDJDict = {}


    global lgrps################毛囊_列表
    lgrps = []


    global crvShapeDict###控制器形状_字典
    crvShapeDict = {}



    mesh = mc.textField('mesh',query = True ,text = True)##########原始网格

    crvShapes = mc.textField('crvShapes',query = True ,text = True)#这里给入shape

    #调用函数执行

    creatfolliceleinvertex(mesh)#网格

    getshape(crvShapes)#必须是curve

    creatfolandctrl()

    ###################################如果是第一次###########################
    mesh = mc.textField('mesh',query = True ,text = True)


    # 复制一份网格
    fakePoly = format('%s_faker' % mesh)
    mc.duplicate(mesh, name=fakePoly, smartTransform=1)

    # 将蒙皮绑定出去
    mc.skinCluster(PDJDict['J_list'], fakePoly, dr=4.5)
    mc.select(mesh)
    mc.select(fakePoly, add=1)
    blendershapename = format('fakershape_%s' % fakePoly)
    mc.blendShape(automatic=1, name=blendershapename)


    #####################获取矩阵######################

    shapes = mc.listRelatives( fakePoly, shapes = True)  # 这里获得了形状节点
    history = mc.listHistory( shapes ,  groupLevels = True , pruneDagObjects = True)  # 这里获得了history
    skins = mc.ls(history , type = 'skinCluster')  # 通过history获得了蒙皮的数据

    # 链接矩阵
    for i in range(len(lgrps)):

        for skin in skins:
            mc.connectAttr('%s.worldInverseMatrix' % PDJDict['D_list'][i] , '%s.bindPreMatrix' % skin + '%s' % [i], f = 1)


    # 建组
    fakegro = 'Faker_Geometry_%s' % mesh
    mc.group(em = 1, name = fakegro)
    mc.parent(fakePoly , fakegro)



##############################如果不是第一次而是额外添加的话##############################
def TwoCluster(*arg):


    global lgrps
    lgrps = []

    global PDJDict
    PDJDict = {}

    global crvShapeDict
    crvShapeDict = {}###控制器形状_字典



    mesh = mc.textField('mesh',query = True ,text = True)##########原始网格

    crvShapes = mc.textField('crvShapes',query = True ,text = True)#这里给入shape

    fakePoly = mc.textField('fakePoly',query = True ,text = True)
    
    #调用函数执行

    creatfolliceleinvertex( mesh )#网格

    getshape( crvShapes )#必须是curve


    creatfolandctrl()

    mc.skinCluster(fakePoly,edit=1,lw = 1 , wt = 0 , ai=PDJDict['J_list'])






####################################################Windows###########################################  
def faker_ui(arg):
    global mesh_textFld
    global crvShapes_textFld
    global fakePoly_textFld
    
    name = 'Faker'

    if mc.window(name,query = True ,exists = True):
        mc.deleteUI(name)
        

    mc.window(name)
    mc.showWindow()

    #????????????????????
    column = mc.columnLayout()
    mc.frameLayout(label = 'Faker_bind')


    #????????????????????????????????????????????

    columns = mc.columnLayout()
    mc.frameLayout(label = '第一步：原始网格')   
    mesh_textFld = mc.textField('mesh',text = 'mesh_name' , 
                                w=200 , editable = 1)
    mc.button(label = '①载入原始网格' , h = 35 ,command = get_mesh)

    mc.setParent(columns)
    columnk = mc.columnLayout()
    mc.frameLayout(label = '第二步：控制器形状')   
    crvShapes_textFld = mc.textField('crvShapes',text = 'crvShapes_name',w=200)
    mc.button(label = '②载入控制器形状', h = 35 , command = get_crvShapes)   

    mc.setParent(columnk)
    columnj = mc.columnLayout()
    mc.frameLayout(label = '第三步：复制体')   
    fakePoly_textFld = mc.textField('fakePoly',text = 'Faker_shape_name',w=200)
    mc.button(label = '③载入复制体', h = 35 , command = get_fakePoly)   

    mc.setParent(columnj)
    #row?????????????????
    mc.rowLayout(numberOfColumns = 4)
    mc.button(label = '根骨' ,
            h = 25 , w = 65 , 
            command = creatroot,
            bgc = [1,0.5,0.4])
    mc.button(label = '初次' ,
            h = 25 , w = 65 , 
            command = firstsecCluster,
            bgc = [0.5,0.8,0.4])
    mc.button(label = '增加' ,
            h = 25 , w = 65 , 
            command  = TwoCluster,
            bgc = [0.5,0.6,1])

####################################################Windows###########################################

    

def get_mesh(*arg):
    q = mc.ls(sl=1)
    add = mc.textField(mesh_textFld, edit=True, text=q[0])

def get_crvShapes(*arg):
    q = mc.ls(sl=1)
    j = mc.listRelatives(q,s=1,pa=1)
    mc.select(j)
    k = mc.ls(sl=1)
    add = mc.textField(crvShapes_textFld, edit=True, text=k[0])

def get_fakePoly(*arg):
    q = mc.ls(sl=1)
    add = mc.textField(fakePoly_textFld, edit=True, text=q[0])



#####################################获得骨骼名称################################
def get_skincluster_jnt(arg):
    MeshLists  = cmds.ls(sl = True)
    cb = len(MeshLists)
    jointsaliens = {}


    for i in range(cb):
        MeshList = MeshLists[i]
        shapes = cmds.listRelatives(MeshList, shapes=True)#这里获得了形状节点，是个列表
        q = [shapes[::2] for t in shapes]
        c = []
        c.extend(q[1])
        history = cmds.listHistory(c, groupLevels=True, pruneDagObjects=True)#这里获得了history，NONE Type
        skins = cmds.ls(history, type='skinCluster')#通过history获得了蒙皮的数据，是个列表
            
            
        for skin in skins:
            joints = cmds.skinCluster(skin, query=True, influence=True)
            jointsarr = [str(r) for r in joints]
            MeshListarr = str(MeshList)
            jointsaliens[MeshListarr] = jointsarr
            print(MeshListarr,jointsarr)
    zx.select(deselect=1)
    for i in MeshLists:
        zx.select(jointsaliens[i],add=1)
    return jointsaliens


############################删除一切只剩下曲线控制器###########################
def only_nurs(arg):
    zx.SelectAllTransforms()
    RiScale = 1
    OL = zx.ls(sl = True)
    Curelists = [str(r) for r in OL]
    for Curelist in Curelists:
        PGlists = Curelist

        zx.setAttr('%s.sx'%PGlists,keyable = True,lock = False)
        zx.setAttr('%s.sy'%PGlists,keyable = True,lock = False)
        zx.setAttr('%s.sz'%PGlists,keyable = True,lock = False)
        
        zx.setAttr('%s.tx'%PGlists,keyable = True,lock = False)
        zx.setAttr('%s.ty'%PGlists,keyable = True,lock = False)
        zx.setAttr('%s.tz'%PGlists,keyable = True,lock = False)
        
        zx.setAttr('%s.rx'%PGlists,keyable = True,lock = False)
        zx.setAttr('%s.ry'%PGlists,keyable = True,lock = False)
        zx.setAttr('%s.rz'%PGlists,keyable = True,lock = False)     
    zx.SelectAllNURBSCurves()
    mel.eval('Unparent;')
    zx.DeleteAllConstraints()
    zx.DeleteAllJoints()
    zx.SelectAllTransforms()
    mel.eval('Unparent;')
    zx.delete()
    zx.SelectAllNURBSCurves()
    zx.makeIdentity(apply=True,s=1)











build_xun_tool_UI()



