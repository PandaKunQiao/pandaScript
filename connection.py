import maya.cmds as cmds
from functools import partial


def get_full_name(name_list, attr_list):
    full_list = []
    for i in xrange(len(name_list)):
        crt_attr_list = []
        for j in xrange(len(attr_list)):
            crt_attr_list += [name_list[i] + "." + attr_list[j]]
        full_list += [crt_attr_list]
    return full_list

def layDrivers(fake_input, parent, row_list = [], name_list = [], parent_list = []):
    driver_list = cmds.ls(selection = True)
    for i in xrange(len(driver_list)):
        name_list += [driver_list[i]]
        parent_list += [cmds.rowLayout(numberOfColumns = 2, 
                                       columnAttach2 = ("both", "both"), 
                                       columnOffset2 = (80, 80),
                                       parent = parent)]
        cmds.text(label = driver_list[i])
        cmds.setParent("..")
    print "driver"
    print name_list
    print parent_list

def layDrivens(fake_input, parent_list, row_list = [], name_list = []):
    driven_list = cmds.ls(selection = True)
    for i in xrange(len(driven_list)):
        name_list += [driven_list[i]]
        cmds.text(label = driven_list[i], parent = parent_list[i])
    print "driven"
    print name_list


def storeDriverAttr(attr_name, text_field_name):
    attr_name += [cmds.textField(text_field_name, query = True, text = True)]
    return None

def storeDrivenAttr(attr_name, text_field_name):
    attr_name += [cmds.textField(text_field_name, query = True, text = True)]
    return None


def connect_chosen(fake_input, drvr_textField_list, 
                               drvn_textField_list,      
                               drvr_trans_list, 
                               drvn_trans_list):
    num_drivenPerDriver = len(drvr_textField_list)
    drvn_attr_list = []
    drvr_attr_list = []

    #take attribute names out of text field
    for i in xrange(num_drivenPerDriver):
        storeDrivenAttr(drvr_attr_list, drvr_textField_list[i])
    for i in xrange(num_drivenPerDriver):
        storeDriverAttr(drvn_attr_list, drvn_textField_list[i])
    driver_full_list = get_full_name(drvr_trans_list, drvr_attr_list)
    driven_full_list = get_full_name(drvn_trans_list, drvn_attr_list)
    print driver_full_list
    print driven_full_list


    for i in xrange(len(driver_full_list[0])):
        for j in xrange(len(driven_full_list)):
            cmds.connectAttr(driver_full_list[j][i], driven_full_list[j][i])
    return None

def first_confirm(fake_input, textField_name, win_name):
    num_of_attr = int(cmds.textField(textField_name, query = True, text = True))
    cmds.deleteUI(win_name)
    win(num_of_attr = num_of_attr)





# window functions


def init_win(fake_input = True):
    winName = "Add Connections"
    versionNumber = 0.1

    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)
    set_num_win = cmds.window(winName, sizeable = True,
                         titleBar = True, resizeToFitChildren = True,
                         menuBar = True, widthHeight = (500, 100),
                         title = winName)
    cmds.columnLayout(columnWidth = 300, rowSpacing = 20)
    cmds.rowLayout(numberOfColumns = 2, columnAttach2 = ("both", "both"), columnOffset2 = (80, 80))
    cmds.text(label = "Number of Attribute to be connected for each node")
    textField_name = cmds.textField(text = "input_number")
    cmds.setParent("..")
    cmds.button(label = "confirm", command = partial(first_confirm, textField_name = textField_name, win_name = set_num_win))
    cmds.showWindow(set_num_win)



def win(fake_input = True, num_of_attr = 1):
    winName = "Add Connections"
    versionNumber = 0.1
    
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)

    connection_win = cmds.window(winName, sizeable = True,
                         titleBar = True, resizeToFitChildren = True,
                         menuBar = True, widthHeight = (500, 500),
                         title = winName)


    #row to confirm driven
    driver_layout = cmds.columnLayout(columnWidth = 300, rowSpacing = 20)
    driver_rows = []
    driver_trans_list = []
    parent_list = []
    driver_rows += [cmds.rowLayout(numberOfColumns=1, 
                                   columnAttach1 = "both", 
                                   columnOffset1 = 170)]
    confirm_drivers_button = cmds.button(label = "Confirm Drivers", 
                                         command = partial(layDrivers, row_list = driver_rows,
                                                                       name_list = driver_trans_list,
                                                                       parent = driver_layout,
                                                                       parent_list = parent_list))

    cmds.setParent("..")
    #rows of driver attribute
    drvr_textField_list = []
    for i in xrange(num_of_attr):
        cmds.rowLayout(numberOfColumns = 1, columnAttach1 = "both",
                                            columnOffset1 = 150)
        textField_drvr_attr = cmds.textField(text = "translateX")
        drvr_textField_list += [textField_drvr_attr]
        cmds.setParent("..")
    

    #row to confirm driven
    driven_layout = cmds.columnLayout(columnWidth = 300, rowSpacing = 20)
    driven_rows = []
    driven_trans_list = []
    driven_rows += [cmds.rowLayout(numberOfColumns=1, 
                                   columnAttach1 = "both", 
                                   columnOffset1 = 170)]
    confirm_drivens_button = cmds.button(label = "Confirm Drivens", 
                                         command = partial(layDrivens, row_list = driven_rows,
                                                                       name_list = driven_trans_list,
                                                                       parent_list = parent_list))
    cmds.setParent("..")



    #rows of driven attribute
    drvn_textField_list = []
    for i in xrange(num_of_attr):
        cmds.rowLayout(numberOfColumns = 1, columnAttach1 = "both",
                                            columnOffset1 = 150)
        textField_drvn_attr = cmds.textField(text = "translateX")
        drvn_textField_list += [textField_drvn_attr]
        cmds.setParent("..")


    #row to confirm all
    cmds.rowLayout(numberOfColumns = 1, columnAttach1 = "both", columnOffset1 = 190)
    cmds.button(label = "Connect", command = partial(connect_chosen, drvr_textField_list = drvr_textField_list,
                                                                     drvn_textField_list = drvn_textField_list,
                                                                     drvr_trans_list = driver_trans_list, 
                                                                     drvn_trans_list = driven_trans_list))
    cmds.showWindow(connection_win)
init_win()