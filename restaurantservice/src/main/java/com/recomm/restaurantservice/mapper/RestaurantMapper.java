package com.recomm.restaurantservice.mapper;

import com.recomm.restaurantservice.dto.RestaurantResponseDTO;
import com.recomm.restaurantservice.model.Restaurant;

public class RestaurantMapper {

    //Get all restaurant details
    public static RestaurantResponseDTO toResponseDTO(Restaurant restaurant){
        RestaurantResponseDTO dto = new RestaurantResponseDTO();
        dto.setPlaceID(restaurant.getPlaceID());
        dto.setLatitude(restaurant.getLatitude());
        dto.setLongitude(restaurant.getLongitude());
        dto.setName(restaurant.getName());
        dto.setState(restaurant.getState());
        dto.setCountry(restaurant.getCountry());
        dto.setAddress(restaurant.getAddress());
        dto.setAlcohol(restaurant.getAlcohol());
        dto.setAccessibility(restaurant.getAccessibility());
        dto.setSmoking_area(restaurant.getSmoking_area());
        dto.setDress_code(restaurant.getDress_code());
        dto.setPrice(restaurant.getPrice());
        dto.setRambience(restaurant.getRambience());
        dto.setFranchise(restaurant.getFranchise());
        dto.setArea(restaurant.getArea());
        dto.setParking_lot(restaurant.getParking_lot());
        dto.setRcuisine(restaurant.getRcuisine());
        return dto;
    }

}
