~/gmsh/gmsh-4.11.0-Linux64/bin/gmsh msh.g -3 -tol 1e-6 -o tmp.msh
source ~/knapsak/env/bin/activate
python cnv_msh.py
