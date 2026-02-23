import { useEffect } from "react";
import { saveLocation } from "../services/api";
import { useAuth } from "../context/useAuth";

export default function useLocation() {
  const { user } = useAuth();

  useEffect(() => {
    if (!user?.access_token) return; 

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        saveLocation(
          {
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
          },
          user.access_token
        );
      },
      () => {
        console.warn("Location permission denied");
      }
    );
  }, [user]); 
}
