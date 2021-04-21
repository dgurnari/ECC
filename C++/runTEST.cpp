#include "compute_local_EC.h"


using namespace std;

int main()
{
    // we input center graph as a list of lists
    // each list corespond to a node and contains its neighbours with distance
    // note, edges are always of the type
    // (i, j) with i<j in the ordering.
    // This is to save space, we do not need the edge (j, i)
    // In practice, we are considering only the upper triangular part
    // of the adjecency matrix

    unsigned id_of_the_center_vertex = 0;
    std::vector< std::pair< unsigned , double > > neigs_of_center_vectex;
    neigs_of_center_vectex.push_back( std::make_pair( 1 , 5.315072906367325 ) );
    neigs_of_center_vectex.push_back( std::make_pair( 2 , 6. ) );
    neigs_of_center_vectex.push_back( std::make_pair( 3 , 5.408326913195984 ) );


    std::vector< std::pair< unsigned , std::vector< std::pair< unsigned , double > > > > neighs_of_neighs_of_centre;
    std::vector< std::pair< unsigned , double > > neighs_of_1;
    neighs_of_1.push_back( std::make_pair( 2 , 4.031128874149275 ) );
    neighs_of_1.push_back( std::make_pair( 3, 6.519202405202649 ) );
    neighs_of_neighs_of_centre.push_back( std::make_pair(1 , neighs_of_1) );

    std::vector< std::pair< unsigned , double > > neighs_of_2;
    neighs_of_2.push_back( std::make_pair(3, 3.3541019662496847) );
    neighs_of_neighs_of_centre.push_back( std::make_pair(2 , neighs_of_2) );

    std::vector< std::pair< unsigned , double > > neighs_of_3;
    // there are none, 3 is the last vertex

    std::vector< std::vector< std::pair< unsigned , double > > > considered_graph;
    considered_graph.push_back(neigs_of_center_vectex);
    considered_graph.push_back(neighs_of_1);
    considered_graph.push_back(neighs_of_2);
    considered_graph.push_back(neighs_of_3);


    std::vector< std::pair< double , int > > ecc = compute_local_EC( considered_graph, true );


    cerr << "Back in main, here is the ECC is: \n";
    for ( size_t i = 0 ; i != ecc.size() ; ++i )
    {
        cerr << ecc[i].first << "  --->  " << ecc[i].second << endl;
    }

    return 0;
}
