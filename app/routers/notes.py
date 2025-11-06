from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.note import NoteReturn, NoteCreate
from app.services.note_service import get_all_notes, get_note_by_id, create_note, update_note, update_archive_status, delete_note_by_id
from app.db.database import get_async_session


router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("", response_model=list[NoteReturn])
async def get_notes(archived: Optional[bool] = None, search: Optional[str] = None, session: AsyncSession = Depends(get_async_session)):
    """
    Получение информации о всех заметках

    Параметры:
    - archived (bool | None): фильтрация по архиву
    - search (str | None): поиск по заголовку
    
    Возвращает:
    - Список данных заметок в формате NoteReturn
    - 404 ошибку если записей нет
    """
    notes = await get_all_notes(session=session)

    filtered_notes = notes
    if search:
        search_lower = search.lower()
        filtered_notes = [
            note for note in filtered_notes
            if search_lower in (note.title or "").lower()
            or search_lower in (note.content or "").lower()
        ]
    if archived is not None:
        filtered_notes = [note for note in filtered_notes if note.is_archived == archived]

    return [
        NoteReturn(
            id=note.id,
            title=note.title,
            content=note.content,
            is_archived=note.is_archived,
            updated_at=note.updated_at,
            created_at=note.created_at
        )
        for note in filtered_notes
    ]

@router.get("/{id}", response_model=NoteReturn)
async def get_note(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Получение информации о заметке по её ID
    
    Параметры:
    - id: идентификатор записи в БД
    
    Возвращает:
    - Данные заметки в формате NoteReturn
    - 404 ошибку если заметка не найдена
    """
    note = await get_note_by_id(id, session=session)

    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    
    return NoteReturn(
        id=note.id,
        title=note.title,
        content=note.content,
        is_archived=note.is_archived,
        updated_at=note.updated_at,
        created_at=note.created_at
    )

@router.post("", status_code=201)
async def create_new__note(note_data: NoteCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Создание новой записи заметки

    Параметры:
    - note_data: данные для создания заметки в формате NoteCreate (поле заголовка обязательно)

    Возвращает:
    - Сообщение об успешном создании записи
    """
    await create_note(note_data, session=session)
    return {"message": "Новая заметка успешно создана!"}

@router.put("/{id}")
async def edit_note(id: int, note_data: NoteCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Частичное обновление данных заметки по ID (PUT-запрос)

    Параметры:
    - id: ID записи в БД
    - note_data: новые данные заметки в формате NoteCreate (поле заголовка обязательно)

    Возвращает:
    - Сообщение об успешном сохранении данных
    - 404 ошибку если заметка не найдена
    """
    updated_note = await update_note(id, note_data, session=session)

    if not updated_note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    
    return {"message": "Изменения сохранены"}

@router.patch("/{id}/archive")
async def archive_note(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Изменение состояния поля is_atchived заметки по ID (PATCH-запрос)

    Параметры:
    - id: ID записи в БД

    Возвращает:
    - Сообщение об успешном обновлении данных
    - 404 ошибку если заметка не найдена
    """
    updated_note = await update_archive_status(id, session=session)

    if not updated_note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    
    status = updated_note.is_archived
    return {"message": f"Заметка перенесена в архив" if status else "Заметка убрана из архива"}

@router.delete("/{id}")
async def delete_note(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Удаление заметки из базы данных по ID.

    Параметры:
    - id: идентификатор записи для удаления

    Возвращает:
    - Сообщение об успешном удалении
    - 404 ошибку если заметка не найдена
    """
    result = await delete_note_by_id(id, session=session)

    if not result:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    
    return {"message": "Заметка удалена"}
