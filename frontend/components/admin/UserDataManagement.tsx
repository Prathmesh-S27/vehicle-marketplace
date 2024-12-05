import React, { useState, useEffect } from 'react';
import { apiClient } from '../../utils/api';

interface User {
  id: number;
  name: string;
  email: string;
  mobileNumber: string;
}

const UserDataManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await apiClient.get('/users');
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users', error);
    }
  };

  const downloadUserData = async () => {
    try {
      const response = await apiClient.get('/users/export', {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'user_data.csv');
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error('Download failed', error);
    }
  };

  return (
    <div>
      <h2>User Data Management</h2>
      <button onClick={downloadUserData}>Download User Data</button>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Mobile Number</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.mobileNumber}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserDataManagement;
