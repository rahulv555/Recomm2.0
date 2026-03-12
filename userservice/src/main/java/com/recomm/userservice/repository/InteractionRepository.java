package com.recomm.userservice.repository;
import org.springframework.stereotype.Repository;
import com.recomm.userservice.model.Interaction;
import com.recomm.userservice.model.InteractionId;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

@Repository
public interface InteractionRepository extends JpaRepository<Interaction, InteractionId>{
// boolean existsById(String id);

 List<Interaction> findAllByUserID(String userID);
}
