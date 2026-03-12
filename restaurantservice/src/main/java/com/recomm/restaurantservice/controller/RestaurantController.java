package com.recomm.restaurantservice.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.recomm.restaurantservice.dto.RatesPlaceNameDTO;
import com.recomm.restaurantservice.dto.RestaurantListRequestDTO;
import com.recomm.restaurantservice.dto.RestaurantRequestDTO;
import com.recomm.restaurantservice.dto.RestaurantResponseDTO;
import com.recomm.restaurantservice.service.RestaurantService;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;



@RestController
@RequestMapping("/restaurant")
public class RestaurantController {
private static final Logger logger = LoggerFactory.getLogger(RestaurantController.class);
    private final RestaurantService restaurantService;

    public RestaurantController(RestaurantService restaurantService){
        this.restaurantService = restaurantService;
    }


    
    @PostMapping()
    public ResponseEntity<RestaurantResponseDTO> getRestaurant(@RequestHeader("X-Authenticated-User-Id") String userId, @RequestBody RestaurantRequestDTO restaurantRequestDTO) {
        
        String placeID = restaurantRequestDTO.getPlaceID();
        
        RestaurantResponseDTO user = restaurantService.getRestaurant(placeID);

        return ResponseEntity.ok().body(user);
    }

    @GetMapping("/rates")
    public ResponseEntity<List<RatesPlaceNameDTO>> getUserRates(@RequestHeader("X-Authenticated-User-Id") String userId) {
         List<RatesPlaceNameDTO> rates = restaurantService.getUserRates(userId);
        return ResponseEntity.ok().body(rates); 
    }

    
    @PostMapping("/list")
     public ResponseEntity<List<RestaurantResponseDTO>> getListRestaurants(@RequestHeader("X-Authenticated-User-Id") String userId, @RequestBody RestaurantListRequestDTO restaurantListRequestDTO) {
        
         List<String> placeIDs = restaurantListRequestDTO.getPlaceIDs();
        
        List<RestaurantResponseDTO> restaurants = restaurantService.getListRestaurants(placeIDs);

        return ResponseEntity.ok().body(restaurants);
    }

    // POST /restaurants/list
{
//   "placeIDs": [2,4,7]
}
}
