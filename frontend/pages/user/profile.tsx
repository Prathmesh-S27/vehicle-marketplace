import React, { useEffect, useState } from 'react';
import { getUserProfile } from '../../utils/api';
import { UserProfile } from '../../types';

const Profile: React.FC = () => {
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const userProfile = await getUserProfile();
                setProfile(userProfile);
            } catch (err) {
                setError('Failed to fetch profile');
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h1>User Profile</h1>
            {profile ? (
                <div>
                    <p><strong>Mobile Number:</strong> {profile.mobile_number}</p>
                    <p><strong>Role:</strong> {profile.role}</p>
                    <p><strong>Created At:</strong> {new Date(profile.created_at).toLocaleString()}</p>
                    <p><strong>Last Login:</strong> {profile.last_login ? new Date(profile.last_login).toLocaleString() : 'Never'}</p>
                </div>
            ) : (
                <p>No profile data available.</p>
            )}
        </div>
    );
};

export default Profile;
