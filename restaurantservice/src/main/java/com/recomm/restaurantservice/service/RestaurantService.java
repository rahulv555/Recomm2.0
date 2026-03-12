package com.recomm.restaurantservice.service;



import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.recomm.restaurantservice.dto.RatesPlaceNameDTO;
import com.recomm.restaurantservice.dto.RestaurantResponseDTO;
import com.recomm.restaurantservice.exception.RestaurantNotFoundException;
import com.recomm.restaurantservice.mapper.InteractionMapper;
import com.recomm.restaurantservice.mapper.RestaurantMapper;
import com.recomm.restaurantservice.model.Interaction;
import com.recomm.restaurantservice.model.Restaurant;
import com.recomm.restaurantservice.repository.InteractionRepository;
import com.recomm.restaurantservice.repository.RestaurantRepository;

@Service
public class RestaurantService {
        private static final Logger logger = LoggerFactory.getLogger(RestaurantService.class);
private final RestaurantRepository restaurantRepository;
private final InteractionRepository interactionRepository;

//Constructor
    public RestaurantService(RestaurantRepository restaurantRepository, InteractionRepository interactionRepository){
        this.restaurantRepository = restaurantRepository;
        this.interactionRepository = interactionRepository;
    }  

    //get specific restaurant by id
    public RestaurantResponseDTO getRestaurant(String placeID){
        Restaurant restaurant = restaurantRepository.findById(placeID).orElseThrow(()->new RestaurantNotFoundException("Restaurant not found with ID: "+ placeID));

        return RestaurantMapper.toResponseDTO(restaurant);

    }


    //get list of restaurants
    public List<RestaurantResponseDTO> getListRestaurants(List<String> placeIDs) {

    List<Restaurant> restaurants = restaurantRepository.findAllById(placeIDs);

    return restaurants.stream()
        .map(r -> RestaurantMapper.toResponseDTO(r))
        .toList();
}


 //Get ratings by a user with restaurant name
 public List<RatesPlaceNameDTO> getUserRates(String userId){

        List<Interaction> rates = interactionRepository.findAllByUserID(userId);



         Set<String> placeIds = rates.stream()
        .map(r -> r.getPlaceId())
        .collect(Collectors.toSet());

        //Fetch all restaurants in ONE query - Map <PlaceID, Name>
        Map<String, String> restaurantNames = restaurantRepository.findAllById(placeIds)
            .stream()
            .collect(Collectors.toMap(r -> r.getPlaceID(), r->r.getName()));

        // Map the DTOs using the map
        return rates.stream()
            .map(r -> InteractionMapper.toResponseDTO(r, restaurantNames.getOrDefault(r.getPlaceId(), "Unknown")))
            .toList();

    }

}
