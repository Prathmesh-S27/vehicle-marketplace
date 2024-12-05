import React, { useState } from 'react';
import SearchComponent from '../components/user/SearchComponent';
import Link from 'next/link';

interface Vehicle {
  id: number;
  model: string;
  type: string;
  images: string[];
}

const HomePage: React.FC = () => {
  const [searchResults, setSearchResults] = useState<Vehicle[]>([]);

  const handleSearchResults = (results: Vehicle[]) => {
    setSearchResults(results);
  };

  return (
    <div className="home-page">
      <h1>Find Your Perfect Vehicle</h1>
      
      <SearchComponent onSearchResults={handleSearchResults} />

      {searchResults.length > 0 && (
        <div className="search-results">
          <h2>Search Results</h2>
          <div className="vehicle-grid">
            {searchResults.map(vehicle => (
              <div key={vehicle.id} className="vehicle-card">
                <img 
                  src={vehicle.images[0]} 
                  alt={vehicle.model} 
                />
                <h3>{vehicle.model}</h3>
                <p>{vehicle.type}</p>
                <Link href={`/user/product/${vehicle.id}`}>
                  View Details
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      <section className="featured-vehicles">
        <h2>Featured Vehicles</h2>
        {/* You can add logic to fetch and display featured vehicles */}
      </section>
    </div>
  );
};

export default HomePage;
