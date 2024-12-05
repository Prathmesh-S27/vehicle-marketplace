import React, { useState, useEffect } from 'react';
import { searchVehicles } from '../../utils/api';
import { Vehicle } from '../../types';

const Search: React.FC = () => {
    const [query, setQuery] = useState<string>('');
    const [vehicles, setVehicles] = useState<Vehicle[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const handleSearch = async () => {
        setLoading(true);
        setError(null);
        try {
            const results = await searchVehicles(query);
            setVehicles(results);
        } catch (err) {
            setError('Failed to fetch vehicles');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (query.length === 0) {
            setVehicles([]);
        }
    }, [query]);

    return (
        <div>
            <h1>Search Vehicles</h1>
            <input
                type="text"
                placeholder="Search by model or type"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button onClick={handleSearch}>Search</button>

            {loading && <div>Loading...</div>}
            {error && <div>{error}</div>}

            <ul>
                {vehicles.map(vehicle => (
                    <li key={vehicle.id}>
                        <strong>{vehicle.model}</strong> - {vehicle.type} - ${vehicle.price}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Search;
