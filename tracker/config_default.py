parameters = {}


# Run parameters
parameters["debug"]=False
parameters["debug_tracker"]=False
parameters["debug_vertexer"]=False
parameters["print_n"]=100
parameters["start_event"]=0
parameters["end_event"]=10000

# Track parameters
parameters["cut_track_HitAddChi2"]=12
parameters["cut_track_HitProjectionSigma"]=7
parameters["cut_track_TrackChi2Reduced"]=3
parameters["cut_track_TrackChi2Prob"]=0.9
parameters["cut_track_TrackNHitsMin"]=3
parameters["cut_track_TrackSpeed"] = [20,40]
parameters["fit_track_MultipleScattering"]=True
parameters["cut_track_MultipleScatteringFind"]=False
parameters["fit_track_Method"]="backward"  #"least-square"

# Vertex parameters
parameters["cut_vertex_SeedDist"]=200
parameters["cut_vertex_SeedChi2"]=100
parameters["cut_vertex_TrackAddDist"]=200
parameters["cut_vertex_TrackAddChi2"]=25
parameters["cut_vertex_TrackDropChi2"]=15
parameters["cut_vertex_VertexChi2ReducedAdd"]=10
parameters["cut_vertex_VertexChi2Reduced"]=7