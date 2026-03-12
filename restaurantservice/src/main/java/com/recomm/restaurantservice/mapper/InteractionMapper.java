package com.recomm.restaurantservice.mapper;

import com.recomm.restaurantservice.dto.RatesPlaceNameDTO;
import com.recomm.restaurantservice.model.Interaction;

public class InteractionMapper {
//For response DTO 
public static RatesPlaceNameDTO toResponseDTO(Interaction inter, String name){
   RatesPlaceNameDTO dto = new RatesPlaceNameDTO();

    dto.setFoodRating(inter.getFoodRating());
    dto.setServiceRating(inter.getServiceRating());
    dto.setRating(inter.getRating());
    dto.setPlaceName(name);
    dto.setPlaceID(inter.getPlaceId());
   
    

    return dto;

}
}
