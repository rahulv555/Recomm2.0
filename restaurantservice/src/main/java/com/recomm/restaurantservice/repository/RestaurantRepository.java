package com.recomm.restaurantservice.repository;
import org.springframework.stereotype.Repository;
import com.recomm.restaurantservice.model.Restaurant;
import org.springframework.data.jpa.repository.JpaRepository;

@Repository
public interface RestaurantRepository extends JpaRepository<Restaurant, String>{
    boolean existsById(String id);
}

