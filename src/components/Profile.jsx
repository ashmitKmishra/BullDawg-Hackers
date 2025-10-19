import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

const Profile = () => {
  const { user, isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <div>Loading ...</div>;
  }

  return (
    isAuthenticated && (
      <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
        <img src={user.picture} alt={user.name} style={{ width: 32, height: 32, borderRadius: '50%' }} />
        <div>
          <h2 style={{ margin: 0, fontSize: '1rem' }}>{user.name}</h2>
          <p style={{ margin: 0, opacity: 0.8 }}>{user.email}</p>
        </div>
      </div>
    )
  );
};

export default Profile;
