# --------------------------------------------------
# User IO for tracker
# The function of this file is to implement the input/output
# --------------------------------------------------
## The following functions needs to be defined:
## 1. load(filename, *args, **kwargs):
##      """
##      Load the data into a dictionary. 
##
##      INPUT:
##      ---
##      filename: str
##          the filename of the input file
##      *args, **kwargs: 
##          additional optional arguments
##
##      Return:
##      ---
##          data: dict
##          The key of the dictionary is the group of hits.
##          For example, there could be three groups, "inactive", "1" and "2"
##          Group "inactive" will not be processed, and can be used to store floor hits
##          Group "1" and "2" can be used to save hits in top layers and wall tracking layers
##      """
## 2. dump(data, filename, *args, **kwargs):
##      Save the processed data to disk. You can implement whatever file format.

import math, os, sys
import importlib

import ROOT as root
import joblib

# Test:
# import importlib
# io_user = importlib.machinery.SourceFileLoader("*", "io_mu-simulation.py").load_module()
# io_user.load("/project/rrg-mdiamond/tomren/mudata/LLP_geometry_40m///SimOutput/MATHUSLA_LLPfiles_HXX/deweighted_LLP_bb_35/20240410/173948/reconstruction_v2.root")  

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
datatypes = importlib.machinery.SourceFileLoader("*", parent_dir+"/datatypes.py").load_module()

def load(filename, printn=2000, *args, **kwargs):
    # Open the file
    tfile = root.TFile.Open(filename)
    tree_name = tfile.GetListOfKeys()[0].GetName()
    Tree = tfile.Get(tree_name)
    branches = [Tree.GetListOfBranches()[i].GetName() for i in range(len(Tree.GetListOfBranches()))]
    entries = Tree.GetEntries()
    print("Opening ROOT file", filename)
    print("  Tree:", tree_name)
    # print("  Branches:", branches)
    print("  Entries:", entries)

    # Make a dictionary
    data = {
        "inactive":[],
        "1":[],
        "2":[],
    }

    # Read the file
    for entry in range(entries):
        if (entry+1)%printn==0:  print("    event is ", entry+1)

        for key in data:
            data[key].append([])

        hits = root_hits_extractor(Tree, entry)
        for hit in hits:
            if  hit.layer<=1 or hit.layer>5:
                data["inactive"][-1].append(hit)            
            elif hit.layer<=5:
                data["1"][-1].append(hit)

    print("Finished loading file")

    # size = getsize(data)
    # print(f"Memory usage of loaded data {size/1e6:.2f} [MB]")

    return data


def dump(data, filename):
    joblib.dump(data,filename+".joblib")
    
    


# ----------------------------------------------------------
# Helper functions
# ----------------------------------------------------------



def c2list(x):
    return [x.at(i) for i in range(x.size())]

def make_hits(x, y, z, t, ylayers):
    Y_LAYERS = ylayers
    det_width  = 4.5 # 4.5cm per bar
    det_height = 1 #[cm]
    time_resolution = 1 #[ns], single channel
    refraction_index = 1.58
    
    unc_trans = det_width/math.sqrt(12)                  
    unc_long = time_resolution*29.979/math.sqrt(2)/refraction_index
    UNC_T = time_resolution/math.sqrt(2) # ns
    UNC_Y = det_height/math.sqrt(12) # uncertainty in thickness, cm
    

    hits=[]
    for i, layer in enumerate(Y_LAYERS):
        if layer%2==1:
            hits.append(datatypes.Hit(x[i], y[i], z[i], t[i], unc_trans, UNC_Y, unc_long, UNC_T, layer, i))
        else:
            hits.append(datatypes.Hit(x[i], y[i], z[i], t[i], unc_long, UNC_Y, unc_trans, UNC_T, layer, i))         
            
    return hits    

def root_hits_extractor(Tree, entry):
    Tree.GetEntry(entry)
    Digi_x = c2list(Tree.Digi_x)
    Digi_y = c2list(Tree.Digi_y)
    Digi_z = c2list(Tree.Digi_z)
    Digi_t = c2list(Tree.Digi_time)
    Digi_layer = c2list(Tree.Digi_layer_id)
    return make_hits(Digi_x, Digi_y, Digi_z, Digi_t, Digi_layer)


from types import ModuleType, FunctionType
from gc import get_referents
def getsize(obj):
    """sum size of object & members."""
    # Custom objects know their class.
    # Function objects seem to know way too much, including modules.
    # Exclude modules as well.

    BLACKLIST = type, ModuleType, FunctionType
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size    
