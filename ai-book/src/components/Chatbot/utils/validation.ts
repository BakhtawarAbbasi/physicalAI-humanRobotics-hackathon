// Validation utilities for the Chatbot UI

export const validateMessageContent = (content: string): { isValid: boolean; error?: string } => {
  if (!content || content.trim().length === 0) {
    return { isValid: false, error: 'Message cannot be empty' };
  }

  if (content.trim().length < 3) {
    return { isValid: false, error: 'Message must be at least 3 characters long' };
  }

  if (content.length > 1000) {
    return { isValid: false, error: 'Message must be less than 1000 characters' };
  }

  return { isValid: true };
};

export const validateUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

export const validateSourceReference = (source: any): { isValid: boolean; error?: string } => {
  if (!source) {
    return { isValid: false, error: 'Source cannot be null or undefined' };
  }

  if (!source.id || typeof source.id !== 'string') {
    return { isValid: false, error: 'Source must have a valid id' };
  }

  if (!source.title || typeof source.title !== 'string' || source.title.length > 200) {
    return { isValid: false, error: 'Source must have a valid title (max 200 characters)' };
  }

  if (!source.url || typeof source.url !== 'string' || !validateUrl(source.url)) {
    return { isValid: false, error: 'Source must have a valid URL' };
  }

  if (!source.snippet || typeof source.snippet !== 'string' || source.snippet.length > 500) {
    return { isValid: false, error: 'Source must have a valid snippet (max 500 characters)' };
  }

  if (typeof source.score !== 'number' || source.score < 0 || source.score > 1) {
    return { isValid: false, error: 'Source must have a valid score between 0 and 1' };
  }

  return { isValid: true };
};

export const validateQueryRequest = (request: any): { isValid: boolean; error?: string } => {
  if (!request) {
    return { isValid: false, error: 'Request cannot be null or undefined' };
  }

  if (!request.query || typeof request.query !== 'string') {
    return { isValid: false, error: 'Request must have a valid query string' };
  }

  const queryValidation = validateMessageContent(request.query);
  if (!queryValidation.isValid) {
    return queryValidation;
  }

  if (request.top_k !== undefined) {
    if (typeof request.top_k !== 'number' || request.top_k < 1 || request.top_k > 10) {
      return { isValid: false, error: 'top_k must be a number between 1 and 10' };
    }
  }

  if (request.conversation_id !== undefined) {
    if (typeof request.conversation_id !== 'string') {
      return { isValid: false, error: 'conversation_id must be a string' };
    }
    // Basic UUID validation (not perfect but catches obvious errors)
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(request.conversation_id)) {
      return { isValid: false, error: 'conversation_id must be a valid UUID' };
    }
  }

  return { isValid: true };
};