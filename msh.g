//
Merge "Cone.stl";
//
DefineConstant[
  // Angle between two triangles above which an edge is considered as sharp
  angle = {90, Min 20, Max 120, Step 1,
    Name "Parameters/Angle for surface detection"},
];
ClassifySurfaces{Pi/2, 1, 1, Pi};
//
CreateGeometry;
Surface Loop(1) = {Surface{:}};
Volume(1) = 1;
Mesh.MeshSizeMax = 20.0;
Mesh.MeshSizeMin = 10.0;
//
