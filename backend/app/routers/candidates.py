    # 4. Process AI: Embedding & Similarity
    clean_text = ai.clean_text(text)
    cv_embedding = ai.get_embedding(clean_text)
    
    role_embedding = role.get_embedding()
    
    if not role_embedding or len(role_embedding) == 0:
         # Fallback if role has no embedding (shouldn't happen but safety)
        score = 0
    else:
        score = ai.calculate_similarity(cv_embedding, role_embedding)

    # 5. Explainability: Extract common keywords
    # Combine role name and description for better context matching
    role_context = f"{role.name} {role.description}"
    matched_skills = ai.extract_keywords(clean_text, role_context)

    # 6. Save Candidate
    db_candidate = models.Candidate(
        role_id=role_id,
        filename=file.filename,
        content=clean_text,
        score=score,
    )
    # cv_embedding is already a list from the new AI engine
    db_candidate.set_embedding(cv_embedding)
    db_candidate.set_matched_skills(matched_skills)
    
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@router.get("/{role_id}", response_model=List[schemas.CandidateResponse])
def get_rankings(
    role_id: int,
    db: Session = Depends(dependencies.get_db)
):
    # Retrieve candidates ordered by score desc
    candidates = db.query(models.Candidate)\
        .filter(models.Candidate.role_id == role_id)\
        .order_by(models.Candidate.score.desc())\
        .all()
    return candidates
