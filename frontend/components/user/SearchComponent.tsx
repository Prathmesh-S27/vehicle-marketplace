import React, { useState } from 'react';
import { apiClient } from '../../utils/api';

interface Vehicle {
  id: number;
  model: string;
  type: string;
  description: string;
  images: string[];
}

interface SearchComponentProps {
  onSearchResults: (results: Vehicle[]) => void;
}

const SearchComponent: React.FC<SearchComponentProps> = ({ onSearchResults }) => {
  const [searchParams, setSearchParams] = useState({
    vehicleType: '',
    model: '',
    keyword: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async () => {
    try {
      const response = await apiClient.get('/vehicles/search', {
        params: searchParams
      });
      onSearchResults(response.data);
    } catch (error) {
      console.error('Search failed', error);
    }
  };

  return (
    <div className="search-container">
      <select
        name="vehicleType"
        value={searchParams.vehicleType}
        onChange={handleInputChange}
      >
        <option value="">All Vehicle Types</option>
        <option value="car">Car</option>
        <option value="truck">Truck</option>
        <option value="motorcycle">Motorcycle</option>
      </select>

      <input
        type="text"
        name="model"
        placeholder="Vehicle Model"
        value={searchParams.model}
        onChange={handleInputChange}
      />

      <input
        type="text"
        name="keyword"
        placeholder="Search keyword"
        value={searchParams.keyword}
        onChange={handleInputChange}
      />

      <button onClick={handleSearch}>Search</button>
    </div>
  );
};

export default SearchComponent;
