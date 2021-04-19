#include "compute_local_EC.h"


using namespace std;

int main()
{
// [[(1, 5.315072906367325), (2, 6.0), (3, 5.408326913195984)],
// [(0, 5.315072906367325), (2, 4.031128874149275), (3, 6.519202405202649)],
// [(0, 6.0), (1, 4.031128874149275), (3, 3.3541019662496847)],
// [(0, 5.408326913195984), (1, 6.519202405202649), (2, 3.3541019662496847)]]

    unsigned id_of_the_center_vertex = 0;
    std::vector< std::pair< unsigned , double > > neigs_of_center_vectex;
    neigs_of_center_vectex.push_back( std::make_pair( 1 , 5.315072906367325 ) );
    neigs_of_center_vectex.push_back( std::make_pair( 2 , 6. ) );
    neigs_of_center_vectex.push_back( std::make_pair( 3 , 5.408326913195984 ) );


    std::vector< std::pair< unsigned , std::vector< std::pair< unsigned , double > > > > neighs_of_neighs_of_centre;
    std::vector< std::pair< unsigned , double > > neighs_of_1;
    neighs_of_1.push_back( std::make_pair( 0 , 5.315072906367325 ) );
    neighs_of_1.push_back( std::make_pair( 2 , 4.031128874149275 ) );
    neighs_of_1.push_back( std::make_pair( 3, 6.519202405202649 ) );
    neighs_of_neighs_of_centre.push_back( std::make_pair(1 , neighs_of_1) );

    std::vector< std::pair< unsigned , double > > neighs_of_2;
    neighs_of_2.push_back( std::make_pair(0, 6.0) );
    neighs_of_2.push_back( std::make_pair(1, 4.031128874149275) );
    neighs_of_2.push_back( std::make_pair(3, 3.3541019662496847) );
    neighs_of_neighs_of_centre.push_back( std::make_pair(2 , neighs_of_2) );

    std::vector< std::pair< unsigned , double > > neighs_of_3;
    neighs_of_3.push_back( std::make_pair(0, 5.408326913195984) );
    neighs_of_3.push_back( std::make_pair(1, 6.519202405202649) );
    neighs_of_3.push_back( std::make_pair(2, 3.3541019662496847) );
    neighs_of_neighs_of_centre.push_back( std::make_pair(3 , neighs_of_3) );


    std::vector< std::pair< double , int > > ecc = compute_local_EC( id_of_the_center_vertex , neigs_of_center_vectex , neighs_of_neighs_of_centre );

    cerr << "Back in main, here is the ECC is: \n";
    for ( size_t i = 0 ; i != ecc.size() ; ++i )
    {
        cerr << ecc[i].first << "  --->  " << ecc[i].second << endl;
    }

    return 0;
}
