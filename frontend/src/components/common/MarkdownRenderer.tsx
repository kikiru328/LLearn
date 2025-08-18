// src/components/common/MarkdownRenderer.tsx
import React from 'react';
import {
  Box,
  Text,
  Heading,
  useColorModeValue,
} from '@chakra-ui/react';

interface MarkdownRendererProps {
  content: string;
  textColor?: string;
  secondaryTextColor?: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ 
  content, 
  textColor: propTextColor, 
  secondaryTextColor: propSecondaryTextColor 
}) => {
  const defaultTextColor = useColorModeValue('gray.900', 'white');
  const defaultSecondaryTextColor = useColorModeValue('gray.600', 'gray.300');
  
  const textColor = propTextColor || defaultTextColor;
  const secondaryTextColor = propSecondaryTextColor || defaultSecondaryTextColor;

  const renderMarkdown = (text: string) => {
    const lines = text.split('\n');
    const elements: React.ReactNode[] = [];
    let currentIndex = 0;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // ## 헤딩 처리
      if (line.startsWith('## ')) {
        elements.push(
          <Heading 
            key={currentIndex++} 
            size="md" 
            color={textColor} 
            mt={6} 
            mb={3}
            fontWeight="bold"
          >
            {line.replace('## ', '')}
          </Heading>
        );
      } 
      // ### 헤딩 처리
      else if (line.startsWith('### ')) {
        elements.push(
          <Heading 
            key={currentIndex++} 
            size="sm" 
            color={textColor} 
            mt={4} 
            mb={2}
            fontWeight="semibold"
          >
            {line.replace('### ', '')}
          </Heading>
        );
      }
      // **굵은 텍스트** 처리
      else if (line.includes('**')) {
        const parts = line.split('**');
        const formattedLine = parts.map((part, index) => 
          index % 2 === 1 ? (
            <Text as="span" key={index} fontWeight="bold" color={textColor}>
              {part}
            </Text>
          ) : (
            <Text as="span" key={index} color={textColor}>
              {part}
            </Text>
          )
        );
        elements.push(
          <Text key={currentIndex++} color={textColor} lineHeight="1.6" mb={2}>
            {formattedLine}
          </Text>
        );
      }
      // - 리스트 처리
      else if (line.startsWith('- ')) {
        elements.push(
          <Box key={currentIndex++} pl={4} mb={1}>
            <Text color={textColor} lineHeight="1.6">
              • {line.replace('- ', '')}
            </Text>
          </Box>
        );
      }
      // 1. 숫자 리스트 처리
      else if (/^\d+\.\s/.test(line)) {
        elements.push(
          <Box key={currentIndex++} pl={4} mb={1}>
            <Text color={textColor} lineHeight="1.6">
              {line}
            </Text>
          </Box>
        );
      }
      // 빈 줄 처리
      else if (line.trim() === '') {
        elements.push(<Box key={currentIndex++} h={3} />);
      }
      // 일반 텍스트
      else if (line.trim()) {
        // 이모지가 포함된 라인 특별 처리
        const hasEmoji = /[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/u.test(line);
        
        elements.push(
          <Text 
            key={currentIndex++} 
            color={textColor} 
            lineHeight="1.6" 
            mb={2}
            fontSize={hasEmoji ? "md" : "sm"}
          >
            {line}
          </Text>
        );
      }
    }

    return elements;
  };

  return <Box>{renderMarkdown(content)}</Box>;
};

export default MarkdownRenderer;

// 사용 예시:
/*
import MarkdownRenderer from '../components/common/MarkdownRenderer';

// 기본 사용
<MarkdownRenderer content={feedback.comment} />

// 커스텀 색상으로 사용
<MarkdownRenderer 
  content={feedback.comment}
  textColor="blue.700"
  secondaryTextColor="blue.500"
/>
*/
