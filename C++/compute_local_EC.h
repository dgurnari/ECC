#include <vector>
#include <set>
#include <map>
#include <utility>
#include <iostream>
#include <algorithm>

using namespace std;

//this is an Euler characteristic curve, as a real valued function with values in integers. This is what we compute locally
inline std::vector< std::pair< double , int > >
compute_local_EC(
//here we pass to the procedure the id of the center vertex
unsigned id_of_the_center_vertex ,
//those are neigs of the center vertex - given as a vector of pairs. The first element of the pair is an id of a vertex (I assumed that this is unsigned int). Second, element of the pair is the distance to that vertex from a centre vertex
const std::vector< std::pair< unsigned , double > >& neigs_of_center_vertex ,
//here, like in the previous case, we pass an information about neighbors of neighnors. we have a vector (of a size = the number of neighbors of the central vertex). Each element of a vector is a pair: id of a neighor and a vector of its neighbors (exactly like neigs_of_center_vectex described above).
const std::vector< std::pair< unsigned , std::vector< std::pair< unsigned , double > > > >& neighs_of_neighs_of_centre )
{
    bool dbg = True;

    //QUESTION, PERHAPS IF WE CONSIDER EDGES FROM LONTEST TO SHORTEST, THEN WE ARE QUARANTEED THAT THE FILTRATION OF THE EDGE == FILTRATION OF THE SIMPLEX. IF THIS IS THE CASE, WE WOULD NOT HAVE TO LOOK FOR IT. THINK ABOUT IT, AND IF IT IS TRUE, ADJUST THE CODE ACCORDINGLY!!

    //first we will introduce a local coordinate system in which centre will be on the first place, and the rest, will be enumerated continuously from 1:
    std::vector< unsigned > vertices_to_consider;
    vertices_to_consider.reserve( neigs_of_center_vertex.size() );
    for ( size_t i = 0 ; i != neigs_of_center_vertex.size() ; ++i )
    {
        if ( id_of_the_center_vertex < neigs_of_center_vertex[i].first )
        {
            vertices_to_consider.push_back( neigs_of_center_vertex[i].first );
        }
    }
    std::sort( vertices_to_consider.begin() , vertices_to_consider.end() );
    if ( dbg )
    {
        cerr << "vertices_to_consider : \n";
        for ( size_t i = 0 ; i != vertices_to_consider.size() ; ++i )cerr << vertices_to_consider[i] << " ";
        cerr << endl;
    }
    //now we create a map from old coordinates to the new one:
    std::map< unsigned , unsigned > old_to_new_map;
    old_to_new_map.insert( std::make_pair( id_of_the_center_vertex , 0 ) );//the central vertex gets mapped to 0
    for ( size_t i = 0 ; i != vertices_to_consider.size() ; ++i )
    {
        old_to_new_map.insert( std::make_pair( vertices_to_consider[i] , i+1 ) );
        if ( dbg ) cerr << "old_to_new_map : " << vertices_to_consider[i] << " --> " << i+1 << endl;
    }
    if ( dbg ) cerr << endl;

    //now we will map all the input data into the local coordiante system:
    std::vector< std::vector< std::pair< unsigned , double > > > considered_graph( vertices_to_consider.size() + 1 );
    //first we map neigs_of_center_vertex
    std::vector< std::pair< unsigned , double > > mapped_center_vertex;
    mapped_center_vertex.reserve( neigs_of_center_vertex.size()     );
    for ( size_t i = 0 ; i != neigs_of_center_vertex.size() ; ++i )
    {
        if ( neigs_of_center_vertex[i].first <=  id_of_the_center_vertex )continue;
        unsigned new_vert = old_to_new_map.find(neigs_of_center_vertex[i].first)->second;
        mapped_center_vertex.push_back( std::make_pair( new_vert , neigs_of_center_vertex[i].second ) );
    }
    considered_graph[0] = mapped_center_vertex;
    if ( dbg )
    {
        cerr << "mapped_center_vertex : \n";
        for ( size_t i = 0 ; i != mapped_center_vertex.size() ; ++i )
        {
            cerr << "( " << mapped_center_vertex[i].first << " " << mapped_center_vertex[i].second << ") ";
        }
        cerr << endl;
    }
    //now let us map the rest:
    for ( size_t i = 0 ; i != neighs_of_neighs_of_centre.size() ; ++i )
    {
        if ( neighs_of_neighs_of_centre[i].first < id_of_the_center_vertex )continue;
        unsigned vertex_we_consider = old_to_new_map.find( neighs_of_neighs_of_centre[i].first )->second;
        std::vector< std::pair< unsigned , double > > new_neigh;
        new_neigh.reserve( neighs_of_neighs_of_centre[i].second.size() );
        if ( dbg ) cerr << "Considering neighs of a vertex : " << neighs_of_neighs_of_centre[i].first << " that is now mapped to : " << vertex_we_consider << endl;
        for ( size_t j = 0 ; j != neighs_of_neighs_of_centre[i].second.size() ; ++j )
        {
            if ( neighs_of_neighs_of_centre[i].second[j].first < id_of_the_center_vertex )continue;
            new_neigh.push_back( std::make_pair( old_to_new_map.find(neighs_of_neighs_of_centre[i].second[j].first)->second , neighs_of_neighs_of_centre[i].second[j].second )  );
            if ( dbg )
            {
                cerr << "Old mapping : (" << neighs_of_neighs_of_centre[i].second[j].first << " , " << neighs_of_neighs_of_centre[i].second[j].second << ") \n";
                cerr << "New mapping : (" << old_to_new_map.find(neighs_of_neighs_of_centre[i].second[j].first)->second << " , " << neighs_of_neighs_of_centre[i].second[j].second << ") \n";
            }
        }
        considered_graph[vertex_we_consider] = new_neigh;
    }



    if ( dbg )
    {
        cerr << "Now we are done with mapping of old to new coordinates. Here is the considered graph: \n";
        for ( size_t i = 0 ; i != considered_graph.size() ; ++i )
        {
            cerr << "i : " << i << endl;
            for ( size_t j = 0 ; j != considered_graph[i].size() ; ++j )
            {
                cerr << "(" << considered_graph[i][j].first << "," << considered_graph[i][j].second << "), ";
            }
            cerr << endl;
        }
    }

    //this is the list of simplices in the current dimension. We will overwrite it everytime we move to a higher dimension.
    std::vector< std::vector< unsigned > > simplices_in_current_dimension;
    simplices_in_current_dimension.reserve( considered_graph.size() );
    //this is a list which tells us what are the filtration values of the simplices in the simplices_in_current_dimension vector. I keed it not in a structure to make the code faster.
    std::vector< double > filtration_of_those_simplices;
    filtration_of_those_simplices.reserve( considered_graph.size() );

    //the value of Euler characteristic will only change at some number of real numbers, equal to the lenth of edges. We will keep in in the structure of a map:
    std::map< double , int > ECC;
    ECC.insert( std::make_pair( 0 , 1 ) );

    //first we will fill in simplices_in_current_dimension vector with the edges from central element to its neighbors with higher id:
    for ( size_t i = 0 ; i != considered_graph[0].size() ; ++i )
    {
        std::vector< unsigned > this_simplex = { 0 , considered_graph[0][i].first };
        simplices_in_current_dimension.push_back( this_simplex );
        filtration_of_those_simplices.push_back( considered_graph[0][i].second );

        //changes to ECC due to those edges:
        if ( dbg )cerr << "######Change of ECC at the level : " << considered_graph[0][i].second  << " by: -1"  << endl;
        std::map< double , int >::iterator it = ECC.find( considered_graph[0][i].second );
        if ( it != ECC.end() )
        {
            double val = it->second;
            val += -1;
            it->second = val;
        }
        else
        {
            ECC.insert( std::make_pair( considered_graph[0][i].second , -1 ) );
        }
    }


    if ( dbg )
    {
        cerr << "simplices_in_current_dimension : \n";
        for ( size_t i = 0 ; i != simplices_in_current_dimension.size() ; ++i )
        {
            cerr << "[";
            for ( size_t j = 0 ; j != simplices_in_current_dimension[i].size() ; ++j )
            {
                cerr << simplices_in_current_dimension[i][j] << ",";
            }
            cerr << "] --> " << filtration_of_those_simplices[i] << endl;
        }
    }

    //We do not need to list the neighbors of the certal vertex, as they are vertices with numbers between 1 and considered_graph[0].size()
    //std::set< unsigned > neighs_of_central_vertex;
    //for ( size_t i = 0 ; i != considered_graph[0].size() ; ++i )
    //{
    //    neighs_of_central_vertex.insert( considered_graph[0][i].first );
    //    if ( dbg )cerr << "Neighs of the central vertex : " << considered_graph[0][i].first << endl;
    //}
    unsigned last_neigh_of_current_vertex = considered_graph[0].size();
    if ( dbg )cerr << "last_neigh_of_current_vertex : " << last_neigh_of_current_vertex << endl;


    //now we can compute all the neighbors of the created 1-dimensional simplices:
    std::vector< std::vector<unsigned> > common_neighs( simplices_in_current_dimension.size() );
    for ( size_t i = 0 ; i != simplices_in_current_dimension.size() ; ++i )
    {
        //we need to check which vertices among neighs_of_neighs_of_centre are common neighs of the vertices in this simplex.
        unsigned the_other_vertex = simplices_in_current_dimension[i][1];
        if ( dbg )cerr << "We will search for the common neighbors of the edge [0," <<  the_other_vertex << "] : \n";
        std::vector< unsigned > neighs;
        neighs.reserve( considered_graph[the_other_vertex].size() );
        if ( dbg )cerr << "The common neigh is : ";
        for ( size_t j = 0 ; j != considered_graph[the_other_vertex].size() ; ++j )
        {
//in this case, it will be not a common neighbor as the index is too high - note that, thanks to the construction above, neighs of the central vertex have indices between 1 and last_neigh_of_current_vertex.
            if ( considered_graph[the_other_vertex][j].first > last_neigh_of_current_vertex  )continue;
            //we do not want to add 0 as a common neighbor as well:
            if ( considered_graph[the_other_vertex][j].first == 0  )continue;
            //in addition, the common neigh have to have higher index than both vertices in the edge:
            if ( considered_graph[the_other_vertex][j].first < the_other_vertex  )continue;
            //if we are here, we have a common neighbor:
            neighs.push_back( considered_graph[the_other_vertex][j].first );
            if ( dbg )cerr << considered_graph[the_other_vertex][j].first << " , ";
        }
        if ( dbg )cerr << endl;
        common_neighs[i] = neighs;
    }

    if ( dbg )
    {
        cerr << "Here is final common_neighs list. \n";
        for ( size_t i = 0 ; i != common_neighs.size() ; ++i )
        {
            cerr << "For the edge : [" << simplices_in_current_dimension[i][0] << "," << simplices_in_current_dimension[i][1] << "] we have the common neighs : ";
            for ( size_t j = 0 ; j != common_neighs[i].size() ; ++j )
            {
                cerr << common_neighs[i][j] << " ";
            }
            cerr << ". Moreover its filtration is : " << filtration_of_those_simplices[i];
            cerr << endl;
        }
    }

    //ToDo, compute the contributio to the Euler characteristic!!! Again, we can optymize it here by not grouping everytihing - each contribution will be at a value of a filtration of an edge - we can perhaps use this fact to accumulate it all in a smart way.


    //We will use this datastructure for quick computations of intersections of neighbor lists
    std::vector< std::set<unsigned> > neighs_of_vertices( considered_graph.size() );
    for ( size_t i = 0 ; i != considered_graph.size() ; ++i )
    {
        std::set< unsigned > neighs_of_this_graph;
        for ( size_t j = 0 ; j != considered_graph[i].size() ; ++j )
        {
            neighs_of_this_graph.insert( considered_graph[i][j].first );
        }
        neighs_of_vertices[i] = neighs_of_this_graph;
    }


    //Now we have created the list of edges, and each of the edge is equipped with common_neighs and all filtration values. Now, we can now create all higher dimensional simplices:
    unsigned dimension = 2;
    int dimm = 1;
    while ( !simplices_in_current_dimension.empty() )
    {
        //first we declare all cointainters that we need.
        std::vector< std::vector< unsigned > > new_simplices_in_current_dimension;
        new_simplices_in_current_dimension.reserve( simplices_in_current_dimension.size() );
        std::vector< double > new_filtration_of_those_simplices;
        new_filtration_of_those_simplices.reserve( filtration_of_those_simplices.size() );
        std::vector< std::vector<unsigned> > new_common_neighs;
        new_common_neighs.reserve( simplices_in_current_dimension.size() );

        //the real computations begins here:
        for ( size_t i = 0 ; i != simplices_in_current_dimension.size() ; ++i )
        {
            // in order to avoid duplicated simplices, lets enforce the ordering of the vertices
            if ( considered_graph[the_other_vertex][j].first < the_other_vertex  )continue;
            if ( dbg )
            {
                cerr << "Consider simplex : [";
                for ( size_t aa = 0 ; aa != simplices_in_current_dimension[i].size() ; ++aa )cerr << simplices_in_current_dimension[i][aa] << ", ";
                cerr << "]. " << endl;
                cerr << "common_neighs[i].size() : " << common_neighs[i].size() << endl;
            }

            //let us check if we can extend simplices_in_current_dimension[i]
            for ( size_t j = 0 ; j !=  common_neighs[i].size() ; ++j )
            {
                if ( dbg )cerr << "It can be extended by adding a vertex : " << common_neighs[i][j] << endl;

                //we can extend simplices_in_current_dimension[i] by adding vertex common_neighs[i][j]
                std::vector< unsigned > new_simplex( dimension+1 );
                for ( size_t k = 0 ; k != dimension ; ++k )new_simplex[k] = simplices_in_current_dimension[i][k];
                new_simplex[dimension] = common_neighs[i][j];
                new_simplices_in_current_dimension.push_back( new_simplex );
                if ( dbg )
                {
                    cerr << "Adding new simplex : ";
                    for ( size_t aa = 0 ; aa != new_simplex.size() ; ++aa )cerr << new_simplex[aa] << " ";
                    cerr << endl;
                }

                //now once we have the new simplex, we need to compute its filtration and common neighs
                //let us start with the filtration. We will set it up initially to the filtration of simplices_in_current_dimension[i]:
                double filtration_of_this_simplex = filtration_of_those_simplices[i];
                for ( size_t k = 0 ; k != simplices_in_current_dimension[i].size() ; ++k )
                {
                    //check what is the weight of an edge from simplices_in_current_dimension[i][k] to common_neighs[i][j]
                    double length_of_this_edge = 0;
                    for ( size_t l = 0 ; l != considered_graph[ simplices_in_current_dimension[i][k] ].size() ; ++l )
                    {
                        if ( considered_graph[ simplices_in_current_dimension[i][k] ][l].first == common_neighs[i][j] )
                        {
                            length_of_this_edge = considered_graph[ simplices_in_current_dimension[i][k] ][l].second;
                            //break;
                        }
                    }
                    if ( length_of_this_edge > filtration_of_this_simplex )filtration_of_this_simplex = length_of_this_edge;
                }
                new_filtration_of_those_simplices.push_back( filtration_of_this_simplex );

                if ( dbg )cerr << "#####Change of ECC at the level : " << filtration_of_this_simplex  << " by: " << dimm << endl;
                std::map< double , int >::iterator it = ECC.find( filtration_of_this_simplex );
                if ( it != ECC.end() )
                {
                    double val = it->second;
                    val += dimm;
                    it->second = val;
                }
                else
                {
                    ECC.insert( std::make_pair( filtration_of_this_simplex , dimm ) );
                }


                if ( dbg )cerr << "The filtration of this simplex is : " << filtration_of_this_simplex << endl;

                //now we still need to deal with the common neighbors.
                std::vector<unsigned> neighs_of_new_simplex;
                neighs_of_new_simplex.reserve( common_neighs[i].size() );
                unsigned new_vertex = common_neighs[i][j];
                for ( size_t k = 0 ; k != common_neighs[i].size() ; ++k )
                {
                    // there seems to be a mistake, there was no k in this loop
                    // I substituted j --> k
                    if ( neighs_of_vertices[new_vertex].find( common_neighs[i][k] ) != neighs_of_vertices[new_vertex].end() )
                    {
                        neighs_of_new_simplex.push_back( common_neighs[i][k] );
                    }
                }
                new_common_neighs.push_back( neighs_of_new_simplex );
            }
        }

        if ( dbg )
        {
            cerr << "Moving to the next dimension, press enter to continue your journey. \n";
            getchar();
        }

        simplices_in_current_dimension = new_simplices_in_current_dimension;
        filtration_of_those_simplices = new_filtration_of_those_simplices;
        common_neighs = new_common_neighs;
        dimension++;
        dimm = dimm*(-1);
    }

    if ( dbg )cerr << "Out of the loop, return result. \n";



    std::vector< std::pair< double , int > > result;
    result.reserve( ECC.size() );
    for ( map< double , int >::iterator it = ECC.begin() ; it != ECC.end() ; ++it )
    {
        if ( dbg ){cerr << it->first << " --> " << it->second << endl;}
        result.push_back( std::make_pair( it->first , it->second ) );
    }

    return result;
}//compute_local_EC
